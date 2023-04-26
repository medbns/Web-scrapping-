from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import requests


headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

product_info=[]
recherche=str(input("entrer votre recherche: "))
ville=str(input("entrer votre ville: "))

x = int(input("the number of page you want: "))
links=[]



for i in range(x):
    url=Request(f'https://www.avito.ma/fr/{ville}/{recherche}-%C3%A0_vendre?f=c&o={i}',headers={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'})
    page_html=urlopen(url).read()
    soup=BeautifulSoup(page_html,'lxml')
   
    table=soup.find('div',{'class':'sc-1nre5ec-0 dBrweF listing'})
    containers=table.find_all('div',{'class':'oan6tk-0 dLOfLV'})
    number=len(containers)
    for i in range(len(containers)):
        product_titre=containers[i].find('span',{'class':'oan6tk-17 ewuNqy'}).text.strip()
        product_prix=containers[i].find('span',{'class':'sc-1x0vz2r-0 izsKzL oan6tk-15 cdJtEx'}).find_all('span')
        if(len(product_prix)==2):
            prix=f"{product_prix[0].text.strip()}  {product_prix[1].text.strip()}"
        else:
            prix="Prix non spécifié"
        product_footer=containers[0].find('div',{'class':'oan6tk-10 iDTQUD'}).find_all('span',{'class':'sc-1x0vz2r-0 hCOOjL'})
        product_ville=f"{product_footer[1].text.strip()}"
        product_posted=f"{product_footer[0].text.strip()}"
        product_categorie=containers[i].find('p',{'class':'sc-1x0vz2r-0 iEJWiq oan6tk-18 bhnuSP'}).text.strip()
        product_links=containers[i].find('a').attrs['href']
        links.append(product_links)
        
        
    for link in links:
    
        url2=requests.get(link,headers=headers)
        page_html=url2.content
        soup=BeautifulSoup(page_html,'lxml')
        barre=soup.find('div',class_='sc-1g3sn3w-4 eTmXXQ')
        product_description=barre.find('p',class_='sc-ij98yj-0 iMUDvH').text.strip()
        product_type=barre.find('span',class_='sc-1x0vz2r-0 jsrimE').text.strip()
        
        product_info.append({"TITRE":product_titre,"PRIX":prix,"CATEGORIE":product_categorie,"VILLE":product_ville,"DATE":product_posted,"Lien de produits":product_links,"DESCRIPTION":product_description,"details":product_type})
   
        
        
            
       
    keys=product_info[0].keys()
    with open("C:/Users/moham/OneDrive/Bureau/data science/avito2.csv",'w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,keys)
        writer.writeheader()
        writer.writerows(product_info)
print("file created")    
