# flushmemc
本程序仅作技术交流，清空互联网服务器的Memcached缓存可能导致目标系统瘫痪，禁止用于非法用途。

## 简介
Memcached反射攻击愈演愈烈，通过本程序可以清空反射源的缓存内容，达到减小攻击流量的目的。

* 特性：

1、伪造源地址

2、使用UDP连接

## 依赖
* Scapy>=2.4.2

pip install scapy

* Flask>=1.0.2

pip install flask

## 使用方法
* python main.py
* 打开 http://127.0.0.1:8080/
* 在文本框每行输入1个 IP:PORT
