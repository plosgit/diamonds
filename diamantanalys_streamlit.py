# Imports
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px

# CSS
st.markdown(
    """
    <style>
        body, .stApp {
            background-color: #000000;
            color: white;
        }
        
        h3 {
            color: white !important;
        }
        
    </style>
    """,
    unsafe_allow_html=True
)

# Graf stil
sns.set_theme(style="whitegrid")

st.markdown(
    """
    <h1 style='color: white;'>Diamantanalys – <span style='color: gold;'>Guldfynd</span></h1>
    """,
    unsafe_allow_html=True
)

# Inledning
st.markdown("""### Inledning

Vi jobbar på Guldfynds IT avdelning och har fått i uppgift att analysera diamanter i python, för att genomföra eventuella investeringar. Vi har fått
tillgång till ett dataset kopplat till just diamanter.

Syftet med denna analys:
- Identifiera faktorer som påverkar diamantpriser
- Hitta lönsamma delar inom produktutbudet
- Skapa strategiska lösningar för företaget

Alla priser visas i dollar
""")

# Laddar datasetet
@st.cache_data
def load_data():
    df = pd.read_csv('diamonds.csv')
    df.rename(columns={"depth": "depth total", "x": "length", "y": "width", "z": "depth"}, inplace=True)
    df.replace(0, pd.NA, inplace=True)
    df.dropna(inplace=True)

    # Ordna clarity
    clarity_order = ["IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2", "SI3", "I1", "I2", "I3"]
    df['clarity'] = pd.Categorical(df['clarity'], categories=clarity_order, ordered=True)

    return df


df = load_data()

st.markdown("""### Detta dataset innehåller över 50,000 diamanter.
Väsentliga variabler: "carat", "cut", "color", "clarity", "price" samt mått (längd, bredd, och djup).
"Cut" och "Clarity" är uppdelad i olika kategorier rangordnat från bäst till sämst:  
#### "Cut":  
"Ideal"  
"Premium"  
"Very Good"  
"Good"  
"Fair"  

#### "Clarity":  
"IF"  
"VVS1"  
"VVS2"  
"VS1"  
"VS2"  
"SI1"  
"S12"  
"S13"  
"I1"  
"I2"  
"I3"

""")

st.markdown("""### Vi börjar nu alanysera diamanter baserat på pris, karat och slipningskvalitet med hjälp av en utökad interaktiv scatterplott.
""")
fig = px.scatter(df, x='carat', y='price', color='cut',hover_data=['color', 'clarity'])
fig.update_layout(plot_bgcolor='white')
st.plotly_chart(fig)

st.markdown("""### Med hjälp av en interaktiv scatterplot kan vi se att priset ökar märkbart med karat. Karat är det som har störst skillnad på pris. Vi kan även se att de orangea prickarna(Fair) ligger lågt dvs dem är billigare medans Ideal, Premium och Very Good är vanligast och ligger lite högre. Vi går vidare genom att analysera antalet diamanter per slipning.
""")

# Diamanter per slipning diagram
fig, ax = plt.subplots()
sns.countplot(data=df, x='cut', order=df['cut'].value_counts().index, hue='cut', palette='pastel', ax=ax, legend=False)
ax.set_title('Antal diamanter per slipning')
ax.set_xlabel('Slipning')
ax.set_ylabel('Antal')

st.pyplot(fig)

st.markdown("""### "Ideal", "Premium" och "Very Good" dominerar utbudet i datasetet. Det visar att dessa slipningar är vanligast bland diamanter. Vi tittar sedan på median priser på dem olika slipningarna.
""")

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df, x='cut', y='price', order=['Fair', 'Good', 'Very Good', 'Premium', 'Ideal'],ax=ax)
ax.set_title('Prisfördelning per Slipning')
ax.set_xlabel('Slipning')
ax.set_ylabel('Pris')
st.pyplot(fig)

st.markdown("""### Boxplotten visar att slipningen "Ideal" har lägst median pris och eftersom vi såg att flest diamanter har slipningen "Ideal" tyder det på att även små och billigare diamanter har stor fokus på bra slipningskvalitet och därmed större efterfrågan.
### Nästa steg blir att analysera genomsnittspris per klarhet och färg i form av en heatmap.""")

pivot = df.pivot_table(index='clarity', columns='color', values='price', aggfunc='mean', observed=False)
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap='YlGnBu', ax=ax)
ax.set_title('Genomsnittligt pris per Klarhet och Färg')
ax.set_xlabel('Färg')
ax.set_ylabel('Klarhet')
st.pyplot(fig)

st.markdown("""### Det vi kan se från vår heatmap är att diamanter med hög klarhet och färg (som IF–D eller VVS1–E) kostar oftast mer, men skillnaderna i pris är inte så stora som man kanske tror. Priserna kan också variera mycket, även för diamanter med samma egenskaper. I nästa steg analyserar vi korrelationer, dvs de värden som driver pris mest.
""")

corr = df[['carat', 'depth total', 'length', 'width', 'depth', 'price']].corr()
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Korrelationsmatris')
st.pyplot(fig)

st.markdown("""### Det vi kan se från vår korrelationsmatris är att karat har starkast samband med pris – ju större karat, desto högre pris (korrelation över 0,9). Även mått som längd, bredd och djup påverkar priset, men inte lika mycket. Faktorer som 'cut', 'color' och 'clarity' har lägre siffror i korrelationen eftersom de är kategoriska värden.

-----------------------------------------------------------------------------------------------------------------------------------------------------

## Summering

### Vi har analyserat diamantdata för att förstå vad som driver pris. Det viktigaste vi såg är att karat (storlek) har störst påverkan – ju större diamant, desto högre pris, och det är inte linjärt utan ökar snabbt.

### Slipningstyperna Ideal, Premium och Very Good är vanligast i marknaden, vilket tyder på att kunder föredrar välslipade stenar. Klarhet och färg påverkar också priset, men variationen är stor – en diamant med lägre klarhet kan ibland vara dyrare än en med högre, beroende på andra faktorer.

### Rekommendation: Guldfynd bör fokusera på att erbjuda diamanter runt 0.5–1.5 carat i populära slipningar (Ideal/Premium), med medelhög klarhet (VS1–SI1). Det ger bra balans mellan pris, marginal och efterfrågan.
""")