require 'formula'
 
class LibdnetPython <Formula
  url 'http://libdnet.googlecode.com/files/libdnet-1.12.tgz'
  homepage 'http://code.google.com/p/libdnet/'
  md5 '9253ef6de1b5e28e9c9a62b882e44cc9'
 
  def install
    ENV["CFLAGS"] = "-O3 -w -pipe"
    system "./configure", "--disable-debug", "--disable-dependency-tracking",
                          "--prefix=#{prefix}",
                          "--mandir=#{man}"
    system "make"
    system "cd python && /usr/bin/python setup.py install"
  end
end
