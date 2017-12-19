# encoding:utf-8
import v2xConfig
import pcap
import dpkt
import re


def main():
    eth_name = v2xConfig.eth_name
    scIP = v2xConfig.scIP
    pc = pcap.pcap(name=eth_name, immediate=True) # 抓取enX
    pc.setfilter('host %s' % scIP)  # 过滤表达式 tcp port 80
    if pc:
        for p_time, p_data in pc:  #
            #print p_data
            try:
                main_pcap(p_time, p_data)
            except:
                continue


def main_pcap(p_time, p_data):  # 解码
    out_format = "%s\t%s\t%s\t%s\t%s\tHTTP/%s"
    p = dpkt.ethernet.Ethernet(p_data)  #
    ret = None
    if p.data.__class__.__name__ == 'IP':
        ip_data = p.data
        src_ip = '%d.%d.%d.%d' % tuple(map(ord, list(ip_data.src)))
        dst_ip = '%d.%d.%d.%d' % tuple(map(ord, list(ip_data.dst)))
        if p.data.data.__class__.__name__ == 'TCP':
            tcp_data = p.data.data
            if tcp_data.data:
                h = dpkt.http.Request(tcp_data.data)  # http解码
                pre = "^/.*$"
                if match(pre, h.uri):  # url 重写
                    http_headers = h.headers
                    host = h.headers['host']
                    url = "http://" + host + h.uri
                else:
                    url = h.uri
                # datetime srcip dstip GET /index.htm HTTP/1.1                       # 输出日志格式
                ret = out_format % (p_time, src_ip, dst_ip, h.method, url, h.version)
                print ret
    return ret

def match(pre, line):
    p = re.compile(pre)
    m = p.match(line)
    return m


if __name__ == '__main__':
    main()