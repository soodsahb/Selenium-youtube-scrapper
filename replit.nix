{ pkgs }: {
  deps = [
    pkgs.glibcLocales
    pkgs.glibc
    pkgs.geckodriver
    pkgs.chromedriver
    pkgs.chromium
    pkgs.libnss3
    
  ];
}