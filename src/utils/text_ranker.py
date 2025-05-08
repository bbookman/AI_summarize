import networkx as nx
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import re

class TextRanker:
    """Text ranking using TextRank algorithm for text summarization."""
    
    def __init__(self, compression_ratio=0.3):
        """
        Initialize the TextRanker with a compression ratio.
        
        Args:
            compression_ratio (float): The ratio of sentences to keep (0.0-1.0)
        """
        self.compression_ratio = compression_ratio
        
        # Download necessary NLTK resources if they don't exist
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            
        try:
            stop_words = stopwords.words('english')
        except LookupError:
            nltk.download('stopwords')
    
    def preprocess_text(self, text):
        """
        Preprocess text by removing special characters and splitting into sentences.
        
        Args:
            text (str): The input text to process
            
        Returns:
            list: List of sentences
        """
        # Remove special characters and digits
        text = re.sub(r'[^\w\s.]', '', text)
        
        # Split text into sentences
        sentences = sent_tokenize(text)
        
        # Filter out very short sentences (likely not informative)
        sentences = [sentence for sentence in sentences if len(sentence.split()) > 3]
        
        return sentences
    
    def create_sentence_vectors(self, sentences):
        """
        Create sentence vectors based on word frequencies.
        
        Args:
            sentences (list): List of preprocessed sentences
            
        Returns:
            list: List of sentence vectors
        """
        # Create a set of all words to build our vocabulary
        all_words = " ".join(sentences).split()
        stop_words = set(stopwords.words('english'))
        vocab = list(set([word.lower() for word in all_words if word.lower() not in stop_words]))
        
        # Create sentence vectors
        sentence_vectors = []
        
        for sentence in sentences:
            words = sentence.split()
            sentence_vector = np.zeros(len(vocab))
            
            # Count word frequencies in the sentence
            for word in words:
                word = word.lower()
                if word not in stop_words and word in vocab:
                    sentence_vector[vocab.index(word)] += 1
            
            sentence_vectors.append(sentence_vector)
            
        return sentence_vectors
    
    def build_similarity_matrix(self, sentence_vectors):
        """
        Build sentence similarity matrix using cosine similarity.
        
        Args:
            sentence_vectors (list): List of sentence vectors
            
        Returns:
            numpy.ndarray: Similarity matrix
        """
        # Check if there are enough sentences to compare
        if not sentence_vectors or len(sentence_vectors) < 2:
            return np.zeros((len(sentence_vectors), len(sentence_vectors)))
            
        # Convert to numpy array for faster computation
        sentence_vectors = np.array(sentence_vectors)
        
        # Handle sparse vectors - if a vector is all zeros, cosine_similarity will cause issues
        # Add a small constant to avoid division by zero
        epsilon = 1e-8
        for i, vec in enumerate(sentence_vectors):
            if np.all(vec == 0):
                sentence_vectors[i] = np.ones(vec.shape) * epsilon
        
        # Calculate cosine similarity between all sentences
        similarity_matrix = cosine_similarity(sentence_vectors)
        
        # Set diagonal to 0 to avoid self-loops in the graph
        np.fill_diagonal(similarity_matrix, 0)
        
        return similarity_matrix
    
    def apply_text_rank(self, similarity_matrix):
        """
        Apply the TextRank algorithm using a similarity matrix.
        
        Args:
            similarity_matrix (numpy.ndarray): Matrix of similarities between sentences
            
        Returns:
            list: Sentence scores
        """
        # Check if similarity matrix is empty
        if similarity_matrix.size == 0:
            return []
            
        # Create the graph
        nx_graph = nx.from_numpy_array(similarity_matrix)
        
        # Apply PageRank algorithm
        try:
            scores = nx.pagerank(nx_graph)
            return scores
        except:
            # If PageRank fails (e.g., due to disconnected graph), return equal weights
            return {i: 1.0 / similarity_matrix.shape[0] for i in range(similarity_matrix.shape[0])}
    
    def extract_summary(self, text):
        """
        Extract a summary from text using the TextRank algorithm.
        
        Args:
            text (str): Text to summarize
            
        Returns:
            str: Summarized text
        """
        if not text:
            return text
            
        # Step 1: Preprocess the text
        sentences = self.preprocess_text(text)
        
        # If there are very few sentences, just return the original text
        if len(sentences) <= 3:
            return text
            
        # Step 2: Create sentence vectors
        sentence_vectors = self.create_sentence_vectors(sentences)
        
        # Step 3: Build the similarity matrix
        similarity_matrix = self.build_similarity_matrix(sentence_vectors)
        
        # Step 4: Apply TextRank to get sentence scores
        sentence_scores = self.apply_text_rank(similarity_matrix)
        
        # Step 5: Select top sentences based on compression ratio
        num_sentences = max(1, int(len(sentences) * self.compression_ratio))
        
        # Sort sentences by score and get the indices
        if isinstance(sentence_scores, dict):  # Handle dict output from nx.pagerank
            ranked_sentences = sorted([(score, idx) for idx, score in sentence_scores.items()], reverse=True)
        else:  # Handle list output
            ranked_sentences = sorted([(score, idx) for idx, score in enumerate(sentence_scores)], reverse=True)
            
        # Select top N sentences
        top_sentence_indices = [idx for _, idx in ranked_sentences[:num_sentences]]
        
        # Sort indices to maintain original text order
        top_sentence_indices.sort()
        
        # Join selected sentences to form summary
        summary = " ".join([sentences[i] for i in top_sentence_indices])
        
        return summary

    def compress_text(self, text, use_textrank=True):
        """
        Compress text using TextRank or simple truncation.
        
        Args:
            text (str): Text to compress
            use_textrank (bool): Whether to use TextRank algorithm or simple truncation
            
        Returns:
            str: Compressed text
        """
        if not text:
            return text
            
        if use_textrank:
            return self.extract_summary(text)
        else:
            # Simple truncation as fallback
            char_limit = int(len(text) * self.compression_ratio)
            return text[:char_limit] + "..." if len(text) > char_limit else text