#############################First scenario all RSUs free -  Server E

#Compute Server E received
traceserver_e_fs<-read.table(file = 'result2/server_h1tf_sta_fn_tt.txt', sep=' ')
names(traceserver_e_fs)<-c("time", "id", "size", "ori", "dest" )
options(drigits.secs = 6)
traceserver_e_fs$time <- as.POSIXlt(traceserver_e_fs$time, origin = "1987-10-05 11:00:00")
traceserver_e_fs$size<- traceserver_e_fs$size*8
sum1segserver_e_fs<-aggregate(list(size = traceserver_e_fs$size), list(segundos = cut(traceserver_e_fs$time, "1 sec")), sum)
mean1segserver_e_fs<-append(list(size = sum1segserver_e_fs$size), list(time = as.numeric(sum1segserver_e_fs$segundos)))

# mean1segserver_e_fs$size[1:157]<- mean1segserver_e_fs$size[1:157]/7
# mean1segserver_e_fs$size[158:235]<- mean1segserver_e_fs$size[158:235]/11
# mean1segserver_e_fs$size[236:300]<- mean1segserver_e_fs$size[236:300]/15

mean1segserver_e_fs$size[1:300]<- mean1segserver_e_fs$size[1:300]/3

pd_e_server<-traceserver_e_fs
pd_e_server$size<-pd_e_server$size/8/1498
sumpd75segserver_e_fs<-aggregate(list(size = pd_e_server$size), list(segundos = cut(pd_e_server$time, "1 sec")), sum)
meanpd75segserver_e_fs<-append(list(size = sumpd75segserver_e_fs$size), list(time = as.numeric(sumpd75segserver_e_fs$segundos)))

#Compute Stations sent Server E
tracecar_e_fs<-read.table(file = 'result2/cartf_fn_5001_tt.txt', sep=' ')
names(tracecar_e_fs)<-c("time", "id", "size", "ori", "dest" )
tracecar_e_fs$time <- as.POSIXlt(tracecar_e_fs$time, origin = "1987-10-05 11:00:00")
tracecar_e_fs$size<- tracecar_e_fs$size*8
sum1segcar_e_fs<-aggregate(list(size = tracecar_e_fs$size), list(segundos = cut(tracecar_e_fs$time, "1 sec")), sum)
mean1segcar_e_fs<-append(list(size = sum1segcar_e_fs$size), list(time =  as.numeric(sum1segcar_e_fs$segundos)))

# mean1segcar_e_fs$size[1:157]<- mean1segcar_e_fs$size[1:157]/7
# mean1segcar_e_fs$size[158:235]<- mean1segcar_e_fs$size[158:235]/11
# mean1segcar_e_fs$size[236:300]<- mean1segcar_e_fs$size[236:300]/15

mean1segcar_e_fs$size[1:300]<- mean1segcar_e_fs$size[1:300]/3

pd_e_car<-tracecar_e_fs
pd_e_car$size<-pd_e_car$size/8/1498
sumpd75segcar_e_fs<-aggregate(list(size = pd_e_car$size), list(segundos = cut(pd_e_car$time, "1 sec")), sum)
meanpd75segcar_e_fs<-append(list(size = sumpd75segcar_e_fs$size), list(time = as.numeric(sumpd75segcar_e_fs$segundos)))

# boxplot(pdr75seg_e_fs[1:4], yaxt="n")
# axis(2, xaxp=c(0.5, 1.3, 10))

#Compute Delay Server E
tracedelay_e_fs<-read.table(file = 'result2/delay_h1_fn_tt.txt')
names(tracedelay_e_fs)<-c("time", "delay")
tracedelay_e_fs$time <- as.POSIXlt(tracedelay_e_fs$time, origin = "1987-10-05 11:00:00")
sum1segdelay_e_fs<-aggregate(list(delay = tracedelay_e_fs$delay), list(segundos = cut(tracedelay_e_fs$time, "1 sec")), sum)
mean1segdelay_e_fs<-append(list(size = sum1segdelay_e_fs$delay), list(time = as.numeric(sum1segdelay_e_fs$segundos)))

mean1segdelay_e_fs$size[1:300]<- mean1segdelay_e_fs$size[1:300]/3

# SH (H1) - sta1, sta4, sta7 - via LTE (AP2)
# GI (H2) - sta2, sta5, sta8 - via D2D (AP3)
# IM (H3) - sta3, sta6, sta9 - via wifi (AP1)

#Plot
par(mar = c(5,5,2,5))
plot(mean1segserver_e_fs$time[1:300], mean1segserver_e_fs$size[1:300], type="l", col="blue", main = "Application H1 (SH) - via LTE", lwd=2, xlim = c(1,300), ylab="Throughput (bps)", ylim = c(0,350000), xlab = "time(s)")
lines(mean1segcar_e_fs$time[1:300], mean1segcar_e_fs$size[1:300], col="red", lwd=2, ylim = c(0,700000))
par(new=T)
plot(mean1segdelay_e_fs$time[1:300], mean1segdelay_e_fs$size[1:300], type="l", col="orange", lwd=2, xlim = c(0,300), axes=F, xlab=NA, ylab=NA, ylim = c(0,1000))
axis(side = 4)
mtext(side = 4, line = 3, 'RTT (ms)')
legend("topleft", legend=c("Server received", "Stations sent", "RTT"), lty=c(1,1,1), col=c("blue", "red", "orange"))

#Compute PDR H1
plot(mean1segserver_e_fs$time[1:300], mean1segserver_e_fs$size[1:300]/mean1segcar_e_fs$size[1:300], type="l", col="blue", main = "Application H1 (SH) - PDR", lwd=2, xlim = c(1,300), ylab="PDR", ylim = c(0,1.1), xlab = "time(s)")

#############################First scenario all RSUs free -  Server G

##Compute Server G received
traceserver_g_fs<-read.table(file = 'result2/server_h2tf_sta_fn_tt.txt', sep=' ')
names(traceserver_g_fs)<-c("time", "id", "size", "ori", "dest" )
options(drigits.secs = 6)
traceserver_g_fs$time <- as.POSIXlt(traceserver_g_fs$time, origin = "1987-10-05 11:00:00")
traceserver_g_fs$size<- traceserver_g_fs$size*8
sum1segserver_g_fs<-aggregate(list(size = traceserver_g_fs$size), list(segundos = cut(traceserver_g_fs$time, "1 sec")), sum)
mean1segserver_g_fs<-append(list(size = sum1segserver_g_fs$size), list(time = as.numeric(sum1segserver_g_fs$segundos)))

mean1segserver_g_fs$size[1:300]<- mean1segserver_g_fs$size[1:300]/3

pd_g_server<-traceserver_g_fs
pd_g_server$size<-pd_g_server$size/8/1498
sumpd75segserver_g_fs<-aggregate(list(size = pd_g_server$size), list(segundos = cut(pd_g_server$time, "75 sec")), sum)
meanpd75segserver_g_fs<-append(list(size = sumpd75segserver_g_fs$size), list(time = as.numeric(sumpd75segserver_g_fs$segundos)))

#Compute Stations sent Server G
tracecar_g_fs<-read.table(file = 'result2/cartf_fn_5002_tt.txt', sep=' ')
names(tracecar_g_fs)<-c("time", "id", "size", "ori", "dest" )
tracecar_g_fs$time <- as.POSIXlt(tracecar_g_fs$time, origin = "1987-10-05 11:00:00")
tracecar_g_fs$size<- tracecar_g_fs$size*8
sum1segcar_g_fs<-aggregate(list(size = tracecar_g_fs$size), list(segundos = cut(tracecar_g_fs$time, "1 sec")), sum)
mean1segcar_g_fs<-append(list(size = sum1segcar_g_fs$size), list(time =  as.numeric(sum1segcar_g_fs$segundos)))

mean1segcar_g_fs$size[1:300]<- mean1segcar_g_fs$size[1:300]/3

pd_g_car<-tracecar_g_fs
pd_g_car$size<-pd_g_car$size/8/1498
sumpd75segcar_g_fs<-aggregate(list(size = pd_g_car$size), list(segundos = cut(pd_g_car$time, "75 sec")), sum)
meanpd75segcar_g_fs<-append(list(size = sumpd75segcar_g_fs$size), list(time = as.numeric(sumpd75segcar_g_fs$segundos)))

# boxplot(pdr75seg_g_fs[1:4], yaxt="n")
# axis(2, xaxp=c(0.5, 1.3, 10))

#Compute Delay Server G
tracedelay_g_fs<-read.table(file = 'result2/delay_h2_fn_tt.txt')
names(tracedelay_g_fs)<-c("time", "delay")
tracedelay_g_fs$time <- as.POSIXlt(tracedelay_g_fs$time, origin = "1987-10-05 11:00:00")
sum1segdelay_g_fs<-aggregate(list(delay = tracedelay_g_fs$delay), list(segundos = cut(tracedelay_g_fs$time, "1 sec")), sum)
mean1segdelay_g_fs<-append(list(size = sum1segdelay_g_fs$delay), list(time = as.numeric(sum1segdelay_g_fs$segundos)))

mean1segdelay_g_fs$size[1:300]<- mean1segdelay_g_fs$size[1:300]/3

#Plot
par(mar = c(5,5,2,5))
plot(mean1segserver_g_fs$time[1:300], mean1segserver_g_fs$size[1:300], type="l", col="blue", main = "Application H2 (GI) - via D2D", lwd=2, xlim = c(1,300), ylab="Throughput (bps)", ylim = c(0,350000), xlab = "time(s)")
lines(mean1segcar_g_fs$time[1:300], mean1segcar_g_fs$size[1:300], col="red", lwd=2, ylim = c(0,700000))
par(new=T)
plot(mean1segdelay_g_fs$time[1:300], mean1segdelay_g_fs$size[1:300], type="l", col="orange", lwd=2, xlim = c(0,300), axes=F, xlab=NA, ylab=NA, ylim = c(0,1000))
axis(side = 4)
mtext(side = 4, line = 3, 'RTT (ms)')
legend("topleft", legend=c("Server received", "Stations sent", "RTT"), lty=c(1,1,1), col=c("blue", "red", "orange"))

#Compute PDR H2
plot(mean1segserver_g_fs$time[1:300], mean1segserver_g_fs$size[1:300]/mean1segcar_g_fs$size[1:300], type="l", col="blue", main = "Application H2 (GI) - PDR", lwd=2, xlim = c(1,300), ylab="PDR", ylim = c(0,1.1), xlab = "time(s)")


###############Server E2

#Compute Server E2 received
traceserver_e2_fs<-read.table(file = 'result2/server_h3tf_sta_fn_tt.txt', sep=' ')
names(traceserver_e2_fs)<-c("time", "id", "size", "ori", "dest" )
options(drigits.secs = 6)
traceserver_e2_fs$time <- as.POSIXlt(traceserver_e2_fs$time, origin = "1987-10-05 11:00:00")
traceserver_e2_fs$size<- traceserver_e2_fs$size*8
sum1segserver_e2_fs<-aggregate(list(size = traceserver_e2_fs$size), list(segundos = cut(traceserver_e2_fs$time, "1 sec")), sum)
mean1segserver_e2_fs<-append(list(size = sum1segserver_e2_fs$size), list(time = as.numeric(sum1segserver_e2_fs$segundos)))

mean1segserver_e2_fs$size[1:300]<- mean1segserver_e2_fs$size[1:300]/3

pd_e2_server<-traceserver_e2_fs
pd_e2_server$size<-pd_e2_server$size/8/1498
sumpd75segserver_e2_fs<-aggregate(list(size = pd_e2_server$size), list(segundos = cut(pd_e2_server$time, "75 sec")), sum)
meanpd75segserver_e2_fs<-append(list(size = sumpd75segserver_e2_fs$size), list(time = as.numeric(sumpd75segserver_e2_fs$segundos)))

#Compute Stations sent Server E2
tracecar_e2_fs<-read.table(file = 'result2/cartf_fn_5003_tt.txt', sep=' ')
names(tracecar_e2_fs)<-c("time", "id", "size", "ori", "dest" )
tracecar_e2_fs$time <- as.POSIXlt(tracecar_e2_fs$time, origin = "1987-10-05 11:00:00")
tracecar_e2_fs$size<- tracecar_e2_fs$size*8
sum1segcar_e2_fs<-aggregate(list(size = tracecar_e2_fs$size), list(segundos = cut(tracecar_e2_fs$time, "1 sec")), sum)
mean1segcar_e2_fs<-append(list(size = sum1segcar_e2_fs$size), list(time =  as.numeric(sum1segcar_e2_fs$segundos)))

mean1segcar_e2_fs$size[1:300]<- mean1segcar_e2_fs$size[1:300]/3

pd_e2_car<-tracecar_e2_fs
pd_e2_car$size<-pd_e2_car$size/8/1498
sumpd75segcar_e2_fs<-aggregate(list(size = pd_e2_car$size), list(segundos = cut(pd_e2_car$time, "75 sec")), sum)
meanpd75segcar_e2_fs<-append(list(size = sumpd75segcar_e2_fs$size), list(time = as.numeric(sumpd75segcar_e2_fs$segundos)))

# boxplot(pdr75seg_e2_fs[1:4], yaxt="n")
# axis(2, xaxp=c(0.5, 1.3, 10))

#Compute Delay Server G
tracedelay_e2_fs<-read.table(file = 'result2/delay_h3_fn_tt.txt')
names(tracedelay_e2_fs)<-c("time", "delay")
tracedelay_e2_fs$time <- as.POSIXlt(tracedelay_e2_fs$time, origin = "1987-10-05 11:00:00")
sum1segdelay_e2_fs<-aggregate(list(delay = tracedelay_e2_fs$delay), list(segundos = cut(tracedelay_e2_fs$time, "1 sec")), sum)
mean1segdelay_e2_fs<-append(list(size = sum1segdelay_e2_fs$delay), list(time = as.numeric(sum1segdelay_e2_fs$segundos)))

mean1segdelay_e2_fs$size[1:300]<- mean1segdelay_e2_fs$size[1:300]/3

#Plot
par(mar = c(5,5,2,5))
plot(mean1segserver_e2_fs$time[1:300], mean1segserver_e2_fs$size[1:300], type="l", col="blue", main = "Application H3 (IM) - via wifi", lwd=2, xlim = c(1,300), ylab="Throughput (bps)", ylim = c(0,250000), xlab = "time(s)")
lines(mean1segcar_e2_fs$time[1:300], mean1segcar_e2_fs$size[1:300], col="red", lwd=2, ylim = c(0,700000))
par(new=T)
plot(mean1segdelay_e2_fs$time[1:300], mean1segdelay_e2_fs$size[1:300], type="l", col="orange", lwd=2, xlim = c(0,300), axes=F, xlab=NA, ylab=NA, ylim = c(0,1000))
axis(side = 4)
mtext(side = 4, line = 3, 'RTT (ms)')
legend("topleft", legend=c("Server received", "Stations sent", "RTT"), lty=c(1,1,1), col=c("blue", "red", "orange"))

#Compute PDR H3
plot(mean1segserver_e2_fs$time[1:300], mean1segserver_e2_fs$size[1:300]/mean1segcar_e2_fs$size[1:300], type="l", col="blue", main = "Application H3 (IM) - PDR", lwd=2, xlim = c(1,300), ylab="PDR", ylim = c(0,1.1), xlab = "time(s)")
