library(lda)
source("cleandata.R")
source("evaluation_measures.R")

corpus<- function(llist){
  
  document<- function(lllist) {
    words_apperance <- c(unlist(strsplit(lllist[[4]], " ")), unlist(strsplit(lllist[[5]], " ")))
    name_appearance <- unlist(lllist[[3]])
    doc <- list(words = words_apperance, name = name_appearance)
    return(doc)
  }
  
  return(lapply(llist, document))
}
doc_corpus<- lapply(data_list, corpus)

allwords_fun<- function(llist) {
  allwords_fun1<- function(lllist) {
    return(c(lllist$name, lllist$words))
  }
  return(lapply(llist, allwords_fun1))
}
doc_allwords<- lapply(doc_corpus, allwords_fun)

vocab_fun<- function(llist) {
  vocab<- c()
  n<- length(llist)
  for(i in 1:n){
    vocab<- c(vocab,llist[[i]])
  }
  vocab<- unique(vocab)
  return(vocab)
}
vocab<- lapply(doc_allwords, vocab_fun)

index<- function(x,a) {return(which(a==x))}
doc_format<- vector("list", 14)
for(i in 1:14) {
  format_fun<- function(lllist) {
    t<- table(lllist)
    vec1<- as.numeric(sapply(names(t), index, a=vocab[[i]]))-1
    vec2<- as.numeric(t)
    m<- matrix(as.integer(c(vec1, vec2)), ncol = 2)
    return(t(m))
  }
  doc_format[[i]] <- lapply(doc_allwords[[i]], format_fun)
}
names(doc_format)<- query.list

# apply LDA
k<- 5
beta <- 0.01
alpha <- k/50
try<- lda.collapsed.gibbs.sampler(doc_format$`A Gupta`,k, vocab$`A Gupta`,
                            num.iterations = 1000, alpha = alpha, eta = beta)

# Calculate topic-word matrix
hw <- try$topics
W <- length(vocab$`A Gupta`)
sum_h <- rowSums(hw)
matrix_sumh <- matrix(rep(sum_h,k),nrow=k,ncol=W)
phi <- (hw+beta)/(matrix_sumh+W*beta)

# Calculate topic-document matrix
hd <- try$document_sums
D <- length(doc_format$`A Gupta`)
sum_hd <- colSums(hd)
matrix_sumhd <- matrix(rep(sum_hd,each=k),nrow=k,ncol=D)
theta <- (hd+alpha)/(matrix_sumhd+k*alpha)

colnames(theta) <- c(1:ncol(theta))
distance<- dist(data.frame(t(theta)))

# Agglomerative Clustering
clust.num<- 26
hcluster <- hclust(distance, "complete")
hclust_id <- cutree(hcluster, k=clust.num)
# plot(hcluster, hang = -1)
# rect.hclust(hcluster, k=k)
showresult<- function(mat) {
  result<- vector("list", clust.num)
  for(i in 1:clust.num) {
    result[[i]]<- names(mat)[mat == i]
  }
  return(result)
}
result<- showresult(hclust_id)

# compute error rate
query.g<- function(llist){
  gold<- function(lllist) {
    gold_id<- lllist[[1]]
    return(gold_id)
  }
  return(sapply(llist, gold))
}
gold_mat<- sapply(data_list, query.g)

match_mat<- matching_matrix(gold_mat[[1]], hclust_id)

performance_statistics(match_mat)


