library(stringr)

data.lib="../data/nameset"
data.files=list.files(path=data.lib, "*.txt")

## remove "*.txt"
query.list=substring(data.files, 1, nchar(data.files)-4)

## add a space
query.list=paste(substring(query.list, 1, 1), 
                 " ", 
                 substring(query.list, 
                           2, nchar(query.list)),
                 sep="")


f.line.proc=function(lin, nam.query="."){
  
  # remove unwanted characters
  char_notallowed <- "\\@#$%^&?" # characters to be removed
  lin.str=str_replace(lin, char_notallowed, "")
  
  # get author id
  lin.str=strsplit(lin.str, "_")[[1]]
  author_id=as.numeric(lin.str[1])
  
  # get paper id
  lin.str=lin.str[2]
  paper_id=strsplit(lin.str, " ")[[1]][1]
  lin.str=substring(lin.str, nchar(paper_id)+1, nchar(lin.str))
  paper_id=as.numeric(paper_id)
  
  # get coauthor list
  lin.str=strsplit(lin.str, "<>")[[1]]
  coauthor_list=strsplit(lin.str[1], ";")[[1]]
  
  #print(lin.str)
  for(j in 1:length(coauthor_list)){
    if(nchar(coauthor_list[j])>0){
      nam = strsplit(coauthor_list[j], " ")[[1]]
      if(nchar(nam[1])>0){
        first.ini=substring(nam[1], 1, 1)
      }else{
        first.ini=substring(nam[2], 1, 1)
      }
    }
    last.name=nam[length(nam)]
    nam.str = paste(first.ini, last.name)
    coauthor_list[j]=nam.str
  }
  
  match_ind = charmatch(nam.query, coauthor_list, nomatch=-1)
  
  #print(nam.query)
  #print(coauthor_list)
  #print(match_ind)
  
  if(match_ind>0){
    
    coauthor_list=coauthor_list[-match_ind]
  }
  
  paper_title=lin.str[2]
  journal_name=lin.str[3]
  
  list(author_id, 
       paper_id, 
       coauthor_list, 
       paper_title, 
       journal_name)
}

data_list=list(1:length(data.files))

for(i in 1:length(data.files)){
  
  ## Step 0 scan in one line at a time.
  
  dat=as.list(readLines(paste(data.lib, data.files[i], sep="/")))
  data_list[[i]]=lapply(dat, f.line.proc, nam.query=query.list[i])
  
}
names(data_list)<- query.list

for(i in 1:14) {
  n<- length(data_list[[i]])
  doc.names<- paste(query.list[i], 1:n, sep = " ") 
  names(data_list[[i]])<- doc.names
}
