require 'formula'
 
class Libpcap <Formula
  url 'git://github.com/mcr/libpcap.git'
  homepage 'http://www.tcpdump.org/'
  version '1.1-PRE-CVS'
 
  def install
    ENV["CFLAGS"] = "-O3 -w -pipe"
    system "./configure", "--prefix=#{prefix}", "--disable-debug", "--disable-dependency-tracking", "--enable-ipv6"
    system "make install"
  end
end
