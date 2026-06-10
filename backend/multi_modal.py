import ollama
from pypdf import PdfReader
import numpy as np
from typing import List, Tuple
import base64
from io import BytesIO
import os
import re
import speech_recognition as sr
from ollama import Client


class PdfProcessing:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):
        reader = PdfReader(self.pdf_path)
        pages = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

        return "\n".join(pages).strip()
    
    def clean_text(self, text: str) -> str:
        text = text.replace("\x00", " ")
        text = re.sub(r"\s+", " ", text)
        return text.strip()


    def chunk_text(self, text: str, chunk_size: int = 250, overlap: int = 50) -> List[str]:
        words = text.split()
        if not words:
            return []

        chunks = []
        start = 0

        while start < len(words):
            end = start + chunk_size
            chunk = " ".join(words[start:end]).strip()
            if chunk:
                chunks.append(chunk)

            if end >= len(words):
                break

            start += chunk_size - overlap

        return chunks
    
    def embed_text(self, text: str, model: str = "nomic-embed-text") -> np.ndarray:
        result = ollama.embeddings(
            model=model,
            prompt=text
        )
        embedding = result["embedding"]
        return np.array(embedding, dtype=np.float32)


    def embed_chunks(self, chunks: List[str], model: str = "nomic-embed-text") -> np.ndarray:
        vectors = [self.embed_text(chunk, model=model) for chunk in chunks]
        return np.vstack(vectors) if vectors else np.array([], dtype=np.float32)


    def cosine_similarity(self, query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        query_norm = np.linalg.norm(query_vec)
        doc_norms = np.linalg.norm(doc_vecs, axis=1)

        denom = (doc_norms * query_norm) + 1e-10
        scores = np.dot(doc_vecs, query_vec) / denom
        return scores


    def build_rag_index(self, pdf_path: str) -> Tuple[List[str], np.ndarray]:
        raw_text = self.extract_text_from_pdf(pdf_path)
        cleaned = self.clean_text(raw_text)
        chunks = self.chunk_text(cleaned)

        if not chunks:
            return [], np.array([], dtype=np.float32)

        embeddings = self.embed_chunks(chunks)
        return chunks, embeddings


    def retrieve_context(
        self,
        question: str,
        chunks: List[str],
        embeddings: np.ndarray,
        top_k: int = 3
    ) -> str:
        if len(chunks) == 0 or embeddings.size == 0:
            return ""

        query_vec = self.embed_text(question)
        scores = self.cosine_similarity(query_vec, embeddings)

        top_indices = np.argsort(scores)[-top_k:][::-1]

        selected_chunks = []
        for idx in top_indices:
            selected_chunks.append(chunks[idx])

        return "\n\n---\n\n".join(selected_chunks)
    

def transcribe_audio(audio_path: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return ""
    
def encode_uploaded_image(uploaded_file) -> tuple[str, str]:
    """
    Encode a Streamlit UploadedFile to base64.
    Returns (base64_string, mime_type).
    """
    mime_type = uploaded_file.type or "image/jpeg"
    image_bytes = uploaded_file.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    return image_b64, mime_type
