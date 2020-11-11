dat = readLines("/home/matthias/Dokumente/BA/data/pan_tsv_AB/chat_length_analysis/all_lengths_n.txt")
l = lapply(dat, as.numeric)
do.call("rbind", l)

#hist(as.numeric(l), breaksbreaks=1:100, labels = TRUE)

library(ggplot2)
ggplot() +
  aes(as.numeric(l)) +
  geom_histogram(binwidth=1, colour="black", fill="white", breaks=seq(1,150,1)) +
  xlab("Number of messages") + ylab("Frequency") +
  scale_x_continuous(breaks=c(1,seq(10,150,10))) +
  scale_y_continuous(breaks=seq(0,65000,5000))


dev.copy(pdf, "/home/matthias/Dokumente/BA/Arbeit/chapters/approach/pan12_number_of_messages_per_chat_hist.pdf", height=3.5, width=7)
dev.off()
# 
# 
# dat = readLines("/home/matthias/Dokumente/BA/data/pan_tsv_AB/chat_length_analysis/all_lengths_words_n.txt")
# lw = lapply(dat, as.numeric)
# do.call("rbind", lw)
# 
# #hist(as.numeric(l), breaksbreaks=1:100, labels = TRUE)
# 
# library(ggplot2)
# ggplot() +
#   aes(as.numeric(lw)) +
#   geom_histogram(binwidth=1, colour="black", fill="white", breaks=seq(1,250,2)) +
#   xlab("Number of words") + ylab("Frequency") +
#   scale_x_continuous(breaks=c(1,seq(0,250,10)))+
#   scale_y_continuous(breaks=seq(0,35000,5000))

