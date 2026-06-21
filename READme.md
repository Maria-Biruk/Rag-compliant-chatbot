# Task 1: Exploratory Data Analysis Summary

The CFPB complaint dataset contains 9,609,797 customer complaint records with 18 attributes. Initial analysis showed that only 2,980,756 records contained consumer complaint narratives, while 6,629,041 records had missing narratives. Since the RAG system depends on textual complaint descriptions, only records with available narratives were considered for further processing.

Complaint distribution analysis showed that financial complaints are concentrated across several product categories, including credit cards, checking and savings accounts, personal loans, and money transfer services. After filtering for the required product categories and removing missing narratives, 355,266 complaint records remained for the RAG pipeline.

Consumer narrative length analysis showed an average complaint length of approximately 200 words, with a median length of 128 words. Some extremely long complaints were identified, with the maximum length reaching 6,469 words, highlighting the need for text chunking during the embedding stage. Text preprocessing was applied by converting narratives to lowercase, removing unnecessary characters, removing boilerplate phrases, and normalizing spacing.

# Task 2: Text Chunking, Embedding, and Vector Store Indexing

## Sampling Strategy

The filtered complaint dataset contained 355,266 complaint narratives across the selected financial product categories. To reduce computational cost while maintaining representative coverage, a stratified sample of 12,000 complaints was created using the Product column as the stratification variable. This ensured that each product category maintained approximately the same proportion in the sample as in the original dataset.

## Chunking Strategy

Customer complaint narratives vary significantly in length, with some complaints exceeding several thousand words. Embedding entire complaints as single vectors may dilute important contextual information and reduce retrieval accuracy. To address this issue, LangChain's RecursiveCharacterTextSplitter was used.

The final configuration used a chunk size of 500 characters with a chunk overlap of 50 characters. This configuration provides a balance between preserving contextual information and generating semantically meaningful chunks while minimizing information loss across chunk boundaries.

The chunking process generated a total of 34,240 text chunks from the 12,000 sampled complaints.

## Embedding Model Selection

The sentence-transformers/all-MiniLM-L6-v2 model was selected as the embedding model. This model generates 384-dimensional sentence embeddings while maintaining a relatively small model size and fast inference speed. It is widely used for semantic search and retrieval applications and provides strong performance for Retrieval-Augmented Generation (RAG) systems.

## Vector Store Creation

Embeddings were generated for all text chunks and stored in a persistent ChromaDB vector database. Each vector was stored alongside metadata including complaint ID, product category, and chunk index. This metadata enables traceability from retrieved chunks back to their original complaints, supporting explainability and evidence-based responses in the final RAG system.
