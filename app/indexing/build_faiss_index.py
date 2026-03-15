import os
import numpy as np
import faiss
from tqdm import tqdm

EMBEDDINGS_DIR = "processed_data/embeddings/chunk_embeddings"
OUTPUT_DIR = "processed_data/vector_index"
INDEX_FILE = os.path.join(OUTPUT_DIR, "faiss_index.bin")


def load_embeddings():
    """
    Load all chunk embeddings into a single numpy array
    """

    embeddings = []

    files = sorted(os.listdir(EMBEDDINGS_DIR))

    for file in tqdm(files, desc="Loading embeddings"):
        if file.endswith(".npy"):
            path = os.path.join(EMBEDDINGS_DIR, file)

            vec = np.load(path)

            embeddings.append(vec)

    embeddings = np.vstack(embeddings).astype("float32")

    return embeddings


def build_index(embeddings):
    """
    Build FAISS index using cosine similarity
    """

    dimension = embeddings.shape[1]

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    # Base index
    index = faiss.IndexFlatIP(dimension)

    # GPU acceleration if available
    if faiss.get_num_gpus() > 0:
        print("Using GPU for FAISS")
        res = faiss.StandardGpuResources()
        index = faiss.index_cpu_to_gpu(res, 0, index)

    print("Adding embeddings to index...")
    index.add(embeddings)

    return index


def save_index(index):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Move to CPU before saving
    if isinstance(index, faiss.IndexPreTransform) or "Gpu" in str(type(index)):
        index = faiss.index_gpu_to_cpu(index)

    faiss.write_index(index, INDEX_FILE)


def main():

    print("Loading embeddings...")
    embeddings = load_embeddings()

    print(f"Total embeddings: {len(embeddings)}")

    print("Building FAISS index...")
    index = build_index(embeddings)

    print("Saving FAISS index...")
    save_index(index)

    print("FAISS index built successfully")


if __name__ == "__main__":
    main()