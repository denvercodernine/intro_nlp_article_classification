from bs4 import BeautifulSoup
with open('souptest.txt', encoding='utf-8') as f:
    s = BeautifulSoup(f.read())
print(s)