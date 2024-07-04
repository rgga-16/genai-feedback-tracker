from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain import hub
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import pandas as pd
import ast, os
from tqdm import tqdm

from embedding import convert_to_embedding, strings_ranked_by_relatedness
from utils import makedir

CWD = os.getcwd()

FILES = [
    {
        "title": "Time-Saver Standards for Interior Design and Space Planning",
        "path": "./finetuning/textbooks/Time-Saver Standards for Interior Design and Space Planning.pdf",
        "remove_pages": list(range(25)) +[255,359,487,488,604,605,606,655,656,692,693,694,756,757,758,1195,1196,1345,1346,1597, 1598,1619]+list(range(1689,1728)),
        "extract_images": False
    },
    {
        "title": "The Interior Design Reference & Specification Book",
        "path": "./finetuning/textbooks/The Interior Design Reference & Specification Book.pdf",
        "remove_pages":[0,1,2,3,4,5,6,7,8,9,10,11,77,135,213,237,267,283,284, 285, 286, 290],
        "extract_images": True
    },
    {
        "title": "Planning And Designers Handbook",
        "path": "./finetuning/textbooks/Planning And Designers Handbook.pdf",
        "remove_pages":[0,1,2,3],
        "extract_images": True
    },
]


def remove_pages_from_pdf(pages, remove_pages):
    return [page for i, page in enumerate(pages) if i not in remove_pages]


def load_document(path, remove_pages, extract_images):
    loader = PyPDFLoader(path,extract_images=extract_images)
    pages = loader.load()
    pages = remove_pages_from_pdf(pages, remove_pages)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200,add_start_index=True)
    texts = text_splitter.split_documents(pages)
    texts = [text.page_content for text in texts]
    return texts

def embed_document(texts):
    embeddings = []
    for text in tqdm(texts):
        embeddings.extend(convert_to_embedding(text))
    return embeddings


def create_document_db():
    save_dir = os.path.join(CWD,"finetuning"); makedir(save_dir)
    document_pickle_path = os.path.join(save_dir, f"document_db.pickle")
    document_hdf5_path = os.path.join(save_dir, f"document_db.hdf5")

    document_db = None

    print("Creating document database")
    
    
    for file in tqdm(FILES):
        texts = load_document(file["path"], file["remove_pages"], file["extract_images"])
        embeddings = embed_document(texts)
        titles=[file["title"]]*len(texts)

        if document_db is None:
            document_db = pd.DataFrame({"text":texts, "embedding":embeddings, "title":titles})
        else: 
            document_db = pd.concat([document_db, pd.DataFrame({"text":texts, "embedding":embeddings, "title":titles})])
    
    if(type(document_db['embedding'][0]) == str):
        document_db['embedding'] =document_db['embedding'].apply(ast.literal_eval)
    if(type(document_db['embedding'][0]) == list and len(document_db['embedding'][0])==1):
        document_db['embedding'] = document_db['embedding'].apply(lambda x: x[0])

    
    document_db.to_hdf(document_hdf5_path, key='document_db', mode='w')
    document_db.to_pickle(document_pickle_path)

    return print("Document database created")


if __name__ == "__main__":
    # create_document_db()
    document_db = pd.read_csv(os.path.join(CWD,"finetuning/document_db.csv"))

    if(type(document_db['embedding'][0]) == str):
        document_db['embedding'] =document_db['embedding'].apply(ast.literal_eval)
    if(type(document_db['embedding'][0]) == list and len(document_db['embedding'][0])==1):
        document_db['embedding'] = document_db['embedding'].apply(lambda x: x[0])

    save_dir = os.path.join(CWD,"finetuning"); makedir(save_dir)
    document_pickle_path = os.path.join(save_dir, f"document_db.pickle")
    document_hdf5_path = os.path.join(save_dir, f"document_db.hdf5")

    document_db.to_hdf(document_hdf5_path, key='document_db', mode='w')
    document_db.to_pickle(document_pickle_path)

    pass
        
    
    
