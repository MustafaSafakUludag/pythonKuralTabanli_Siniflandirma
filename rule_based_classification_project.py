
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama


#############################################
# İş Problemi
#############################################
# Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak seviye tabanlı (level based) yeni müşteri tanımları (persona)
# oluşturmak ve bu yeni müşteri tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete
# ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.

# Örneğin: Türkiye’den IOS kullanıcısı olan 25 yaşındaki bir erkek kullanıcının ortalama ne kadar kazandırabileceği belirlenmek isteniyor.



#############################################
# Veri Seti Hikayesi
#############################################
# Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını ve bu ürünleri satın alan kullanıcıların bazı
# demografik bilgilerini barındırmaktadır. Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo
# tekilleştirilmemiştir. Diğer bir ifade ile belirli demografik özelliklere sahip bir kullanıcı birden fazla alışveriş yapmış olabilir.

# Price: Müşterinin harcama tutarı
# Source: Müşterinin bağlandığı cihaz türü
# Sex: Müşterinin cinsiyeti
# Country: Müşterinin ülkesi
# Age: Müşterinin yaşı


################# Uygulama Öncesi #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# Uygulama Sonrası #####################

#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C


#############################################
# PROJE GÖREVLERİ
#############################################

#############################################
# GÖREV 1: Aşağıdaki soruları yanıtlayınız.
#############################################


# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import pandas as pd
pd.set_option("display.max_rows", None)
df = pd.read_csv('Datasets/persona.csv')

def check_df(dataframe, head=4, tail=4):
    print("##################### Shape #####################")
    print(dataframe.shape)

    print("##################### Types #####################")
    print(dataframe.dtypes)

    print("##################### Head #####################")
    print(dataframe.head(head))

    print("##################### Tail #####################")
    print(dataframe.tail(tail))

    print("##################### NA #####################")
    print(dataframe.isnull().sum())

    print("##################### Quantiles #####################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)
print("*"*100)


print(df.head())
"""
   PRICE   SOURCE   SEX COUNTRY  AGE
0     39  android  male     bra   17
1     39  android  male     bra   17
2     49  android  male     bra   17
3     29  android  male     tur   17
4     49  android  male     tur   17
"""
print(df.shape)
"""
(5000, 5)
"""
print(df.info())
"""
<class 'pandas.core.frame.DataFrame'>
Int64Index: 5000 entries, 0 to 4999
Data columns (total 5 columns):
 #   Column   Non-Null Count  Dtype 
---  ------   --------------  ----- 
 0   PRICE    5000 non-null   int64 
 1   SOURCE   5000 non-null   object
 2   SEX      5000 non-null   object
 3   COUNTRY  5000 non-null   object
 4   AGE      5000 non-null   int64 
dtypes: int64(2), object(3)
memory usage: 234.4+ KB
"""

# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?

print(df["SOURCE"].nunique())
"""
2
"""
print(df["SOURCE"].value_counts())
"""
android    2974
ios        2026
Name: SOURCE, dtype: int64
"""

# Soru 3: Kaç unique PRICE vardır?

print(df["PRICE"].unique())
"""
[39 49 29 19 59  9]
"""
print(df["PRICE"].nunique())
"""
6
"""

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?

print(df["PRICE"].value_counts())
"""
29    1305
39    1260
49    1031
19     992
59     212
9      200
Name: PRICE, dtype: int64
"""
# Soru 5: Hangi ülkeden kaçar tane satış olmuş?

print(df["COUNTRY"].value_counts())
"""
usa    2065
bra    1496
deu     455
tur     451
fra     303
can     230
Name: COUNTRY, dtype: int64
"""
print(df.groupby("COUNTRY")["PRICE"].count())
"""
COUNTRY
bra    1496
can     230
deu     455
fra     303
tur     451
usa    2065
Name: PRICE, dtype: int64
"""
print(df.pivot_table(values="PRICE",index="COUNTRY",aggfunc="count"))
"""
         PRICE
COUNTRY       
bra       1496
can        230
deu        455
fra        303
tur        451
usa       2065
"""

# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?

print(df.groupby("COUNTRY")["PRICE"].sum())
"""
COUNTRY
bra    51354
can     7730
deu    15485
fra    10177
tur    15689
usa    70225
Name: PRICE, dtype: int64
"""
print(df.groupby("COUNTRY").agg({"PRICE": "sum"}))
"""
         PRICE
COUNTRY       
bra      51354
can       7730
deu      15485
fra      10177
tur      15689
usa      70225
"""
print(df.pivot_table(values="PRICE",index="COUNTRY",aggfunc="sum"))
"""
         PRICE
COUNTRY       
bra      51354
can       7730
deu      15485
fra      10177
tur      15689
usa      70225
"""

# Soru 7: SOURCE türlerine göre göre satış sayıları nedir?

print(df["SOURCE"].value_counts())
"""
android    2974
ios        2026
Name: SOURCE, dtype: int64
"""
# Soru 8: Ülkelere göre PRICE ortalamaları nedir?

print(df.groupby(by=['COUNTRY']).agg({"PRICE": "mean"}))
"""
             PRICE
COUNTRY           
bra      34.327540
can      33.608696
deu      34.032967
fra      33.587459
tur      34.787140
usa      34.007264
"""
# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?

print(df.groupby(by=['SOURCE']).agg({"PRICE": "mean"}))
"""
             PRICE
SOURCE            
android  34.174849
ios      34.069102
"""
# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

print(df.groupby(by=["COUNTRY", 'SOURCE']).agg({"PRICE": "mean"}))
"""
                     PRICE
COUNTRY SOURCE            
bra     android  34.387029
        ios      34.222222
can     android  33.330709
        ios      33.951456
deu     android  33.869888
        ios      34.268817
fra     android  34.312500
        ios      32.776224
tur     android  36.229437
        ios      33.272727
usa     android  33.760357
        ios      34.371703
"""

#############################################
# GÖREV 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################


print(df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).head())
"""
                                PRICE
COUNTRY SOURCE  SEX    AGE           
bra     android female 15   38.714286
                       16   35.944444
                       17   35.666667
                       18   32.255814
                       19   35.206897
"""

#############################################
# GÖREV 3: Çıktıyı PRICE'a göre sıralayınız.
#############################################
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.


agg_df = df.groupby(by=["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
print(agg_df.head())
"""
                            PRICE
COUNTRY SOURCE  SEX    AGE       
bra     android male   46    59.0
usa     android male   36    59.0
fra     android female 24    59.0
usa     ios     male   32    54.0
deu     android female 36    49.0
"""

#############################################
# GÖREV 4: Indekste yer alan isimleri değişken ismine çeviriniz.
#############################################
# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çeviriniz.
# İpucu: reset_index()
# agg_df.reset_index(inplace=True)


agg_df = agg_df.reset_index()
print(agg_df.head())
"""
  COUNTRY   SOURCE     SEX  AGE  PRICE
0     bra  android    male   46   59.0
1     usa  android    male   36   59.0
2     fra  android  female   24   59.0
3     usa      ios    male   32   54.0
4     deu  android  female   36   49.0
"""

#############################################
# GÖREV 5: AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
#############################################
# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici olacağını düşündüğünüz şekilde oluşturunuz.
# Örneğin: '0_18', '19_23', '24_30', '31_40', '41_70'

#İlgili değişken için bölme işlemi yapacağız böylece yoğunluk hangi yaş aralığında min. max. değerlerine ulaşmış olacağız.


print(agg_df["AGE"].describe())
"""
count    348.000000
mean      28.258621
std       11.379075
min       15.000000
25%       19.000000
50%       25.000000
75%       34.000000
max       66.000000
"""
# AGE değişkeninin nerelerden bölüneceğini belirtelim:

bins = [0, 18, 23, 30, 40, agg_df["AGE"].max()]

# Bölünen noktalara karşılık isimlendirmelerin ne olacağını ifade edelim:

mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())]

# age'i bölelim:
#yeni bir değişken oluşturduk cut methoduyla ilili değişkeni bölme işlemi gerçekleştirdik.
#yukarıdaki aralıklara göre bölme işlemi ve label işlemlerinin yapılmasını istedik.

agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins, labels=mylabels)
print(agg_df.head())
"""
  COUNTRY   SOURCE     SEX  AGE  PRICE age_cat
0     bra  android    male   46   59.0   41_66
1     usa  android    male   36   59.0   31_40
2     fra  android  female   24   59.0   24_30
3     usa      ios    male   32   54.0   31_40
4     deu  android  female   36   49.0   31_40
"""

#############################################
# GÖREV 6: Yeni level based müşterileri tanımlayınız ve veri setine değişken olarak ekleyiniz.
#############################################
# customers_level_based adında bir değişken tanımlayınız ve veri setine bu değişkeni ekleyiniz.
# Dikkat!
# list comp ile customers_level_based değerleri oluşturulduktan sonra bu değerlerin tekilleştirilmesi gerekmektedir.
# Örneğin birden fazla şu ifadeden olabilir: USA_ANDROID_MALE_0_18
# Bunları groupby'a alıp price ortalamalarını almak gerekmektedir.





# YÖNTEM 1
# değişken isimleri:
print(agg_df.columns)
"""Index(['COUNTRY', 'SOURCE', 'SEX', 'AGE', 'PRICE', 'age_cat'],dtype='object')"""
# gözlem değerlerine nasıl erişiriz?
for row in agg_df.values:
    print(row)
"""
['bra' 'android' 'male' 46 59.0 '41_66']
['usa' 'android' 'male' 36 59.0 '31_40']
['fra' 'android' 'female' 24 59.0 '24_30']
['usa' 'ios' 'male' 32 54.0 '31_40']
['deu' 'android' 'female' 36 49.0 '31_40']
"""
# COUNTRY, SOURCE, SEX ve age_cat değişkenlerinin DEĞERLERİNİ yan yana koymak ve alt tireyle birleştirmek istiyoruz.
# Bunu list comprehension ile yapabiliriz.
# Yukarıdaki döngüdeki gözlem değerlerinin bize lazım olanlarını seçecek şekilde işlemi gerçekletirelim:
[print(row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper()) for row in agg_df.values]
"""
BRA_ANDROID_MALE_41_66
USA_ANDROID_MALE_31_40
FRA_ANDROID_FEMALE_24_30
USA_IOS_MALE_31_40
DEU_ANDROID_FEMALE_31_40
"""

# Veri setine ekleyelim:
agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
print(agg_df.head())
"""
  COUNTRY   SOURCE     SEX  AGE  PRICE age_cat     customers_level_based
0     bra  android    male   46   59.0   41_66    BRA_ANDROID_MALE_41_66
1     usa  android    male   36   59.0   31_40    USA_ANDROID_MALE_31_40
2     fra  android  female   24   59.0   24_30  FRA_ANDROID_FEMALE_24_30
3     usa      ios    male   32   54.0   31_40        USA_IOS_MALE_31_40
4     deu  android  female   36   49.0   31_40  DEU_ANDROID_FEMALE_31_40
"""

agg_df = agg_df[["customers_level_based", "PRICE"]]
print(agg_df.head())
"""
      customers_level_based  PRICE
0    BRA_ANDROID_MALE_41_66   59.0
1    USA_ANDROID_MALE_31_40   59.0
2  FRA_ANDROID_FEMALE_24_30   59.0
3        USA_IOS_MALE_31_40   54.0
4  DEU_ANDROID_FEMALE_31_40   49.0
"""

for i in agg_df["customers_level_based"].values:
    print(i.split("_"))
"""
['BRA', 'ANDROID', 'MALE', '41', '66']
['USA', 'ANDROID', 'MALE', '31', '40']
['FRA', 'ANDROID', 'FEMALE', '24', '30']
['USA', 'IOS', 'MALE', '31', '40']
['DEU', 'ANDROID', 'FEMALE', '31', '40']
"""

# Amacımıza bir adım daha yaklaştık.
# Burada ufak bir problem var. Birçok aynı segment olacak.
# örneğin USA_ANDROID_MALE_0_18 segmentinden birçok sayıda olabilir.
# kontrol edelim:
print(agg_df["customers_level_based"].value_counts())
"""
BRA_ANDROID_MALE_24_30      7
USA_ANDROID_MALE_41_66      7
USA_IOS_FEMALE_24_30        7
BRA_ANDROID_FEMALE_24_30    7
USA_ANDROID_MALE_24_30      7
BRA_IOS_MALE_31_40          6
USA_ANDROID_FEMALE_24_30    6
Name: customers_level_based, dtype: int64
                              PRICE
"""
# Bu sebeple segmentlere göre groupby yaptıktan sonra price ortalamalarını almalı ve segmentleri tekilleştirmeliyiz.
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
print(agg_df)
"""
customers_level_based              
BRA_ANDROID_FEMALE_0_18   35.645303
BRA_ANDROID_FEMALE_19_23  34.077340
BRA_ANDROID_FEMALE_24_30  33.863946
BRA_ANDROID_FEMALE_31_40  34.898326
BRA_ANDROID_FEMALE_41_66  36.737179
"""
# customers_level_based index'te yer almaktadır. Bunu değişkene çevirelim.
agg_df = agg_df.reset_index()
print(agg_df.head())
"""
      customers_level_based      PRICE
0   BRA_ANDROID_FEMALE_0_18  35.645303
1  BRA_ANDROID_FEMALE_19_23  34.077340
2  BRA_ANDROID_FEMALE_24_30  33.863946
3  BRA_ANDROID_FEMALE_31_40  34.898326
4  BRA_ANDROID_FEMALE_41_66  36.737179
"""
# kontrol edelim. her bir persona'nın 1 tane olmasını bekleriz:
print(agg_df["customers_level_based"].value_counts())
print(agg_df.head())

#############################################
# GÖREV 7: Yeni müşterileri (USA_ANDROID_MALE_0_18) segmentlere ayırınız.
#############################################
# PRICE'a göre segmentlere ayırınız,
# segmentleri "SEGMENT" isimlendirmesi ile agg_df'e ekleyiniz,
# segmentleri betimleyiniz,
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
print(agg_df.head())
"""
      customers_level_based      PRICE SEGMENT
0   BRA_ANDROID_FEMALE_0_18  35.645303       B
1  BRA_ANDROID_FEMALE_19_23  34.077340       C
2  BRA_ANDROID_FEMALE_24_30  33.863946       C
3  BRA_ANDROID_FEMALE_31_40  34.898326       B
4  BRA_ANDROID_FEMALE_41_66  36.737179       A
"""
print(agg_df.groupby("SEGMENT").agg({"PRICE": "mean"}))
"""
             PRICE
SEGMENT           
D        29.206780
C        33.509674
B        34.999645
A        38.691234
"""

#############################################
# GÖREV 8: Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "TUR_ANDROID_FEMALE_31_40"
print(agg_df[agg_df["customers_level_based"] == new_user])
"""
       customers_level_based      PRICE SEGMENT
72  TUR_ANDROID_FEMALE_31_40  41.833333       A
"""
# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "FRA_IOS_FEMALE_31_40"
print(agg_df[agg_df["customers_level_based"] == new_user])
"""
   customers_level_based      PRICE SEGMENT
63  FRA_IOS_FEMALE_31_40  32.818182       C
"""


def new(agg_df, new_user):
    print(agg_df[agg_df["customers_level_based"]== new_user])

new(agg_df,"TUR_ANDROID_FEMALE_31_40")

new(agg_df,"FRA_IOS_FEMALE_31_40")

