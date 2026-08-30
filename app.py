import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Mobile-optimized layout
st.set_page_config(page_title="SKSSF Sprint | Live Portal", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 1. SECURITY & AUTHENTICATION MAPPING
# ==========================================
COORDINATORS = {
    "7356941375": {"name": "Admin Mishab", "unit": "ALL"},
    "9946525451": {"name": "MUHAMMED SHIBIL MP", "unit": "CHANJAL"},
    "8848335940": {"name": "NASEEM", "unit": "CHANTHAPPARAMBA"},
    "7736620819": {"name": "MOHAMMED SHIBILI", "unit": "PONMALA MELMURI"},
    "8129468085": {"name": "MOHAMMED YASIR", "unit": "VAZHENGAL"},
    "8136860910": {"name": "MOHAMMED RISHAL AP", "unit": "VAZHENGAL"},
    "8137981833": {"name": "RABEEHU RAHMAN", "unit": "PONMALA PALLIPPADI"},
    "9605534951": {"name": "MUHAMMAD SALIM PK", "unit": "PONMALA PALLIPPADI"},
    "9207250414": {"name": "SALMANUL FARIS KK", "unit": "PANG THANIKKODE"},
    "8714118823": {"name": "M.P MUHAMMED SHAFEEQ FAIZY", "unit": "CHAPPANANGADI"},
    "9544658384": {"name": "MOHAMED MUNEER", "unit": "CHAPPANANGADI"},
    "9567300820": {"name": "SIRAJUDHEEN KC", "unit": "CHAPPANANGADI"},
    "7907818381": {"name": "JASEELMP", "unit": "NORTH PANG"},
    "9074844872": {"name": "MUHAMMED NIYAS", "unit": "VATTAPPARAMBA"},
    "9037282624": {"name": "IRSHAD ALI T", "unit": "VATTAPPARAMBA"},
    "7561000900": {"name": "NIZAMUDHEEN M", "unit": "VATTAPPARAMBA"},
    "9809512129": {"name": "SHIHAB WAFY MC", "unit": "PALLIPPARAMBA"},
    "7012721664": {"name": "MUHAMMED FAKRUDHEEN", "unit": "PARANGIMOOCHIKKAL"},
    "9747394649": {"name": "SAYYID JALALUDHEEN HUDAWI", "unit": "PARANGIMOOCHIKKAL"},
    "8590866480": {"name": "MUHAMMED FASEEH T", "unit": "CHANDHANAPARAMBA"},
    "8606709200": {"name": "HSSAN MAHMOOD KV", "unit": "PANG THORA"},
    "9747888446": {"name": "MUHAMMED MUSTHAFA VP", "unit": "PANG THORA"},
    "9633777058": {"name": "MOHAMMED AMIR", "unit": "PANG THORA"},
    "9946792480": {"name": "MUHAMMED FAYIS M P", "unit": "VADAKKEKULAMB"},
    "9061616266": {"name": "MOHAMED YASEEN FAIZY", "unit": "VADAKKEKULAMB"},
    "7510246924": {"name": "MUHAMMAD FAYIS ANWARI", "unit": "WEST PANG"},
    "9947029629": {"name": "ABDUL AZEEZ", "unit": "WEST PANG"},
    "9947271399": {"name": "SIDHEEQUE FAIZY P K", "unit": "PADAPPARAMBA"},
    "8075652110": {"name": "MUSTHAFA KT", "unit": "PADAPPARAMBA"},
    "9061973092": {"name": "MUHAMMAD RAFEEQ KAMALI", "unit": "NELLOLIPPARAMBA"},
    "9048387762": {"name": "MOHAMMED SINAN", "unit": "NELLOLIPPARAMBA"},
    "9946376846": {"name": "MUHAMMAD SAKEER FAIZY M", "unit": "EAST PANG"},
    "9048808053": {"name": "MAHFOOL PT", "unit": "EAST PANG"},
    "9961982661": {"name": "SAYYID FASAL THANGAL", "unit": "EAST PANG"},
    "9846808859": {"name": "MOHAMMED SAFVAN PT", "unit": "PONMALA THENPARAMBA"},
    "7034029572": {"name": "MOHAMMED KABEER BISHRI PM", "unit": "PONMALA THENPARAMBA"},
    "9895598821": {"name": "SULFEEKAR ALI PT", "unit": "PONMALA THENPARAMBA"},
    "8921722584": {"name": "MUHAMMED SINAN PT", "unit": "PONMALA THENPARAMBA"},
    "8606002161": {"name": "MUHAMMED SHAMNAD", "unit": "PONMALA EAST"},
    "7356134895": {"name": "MOHAMED DHILSHAD VILLEN", "unit": "PONMALA EAST"},
    "8078052921": {"name": "ABDUL HAKEEM KT", "unit": "PONMALA EAST"},
    "9048523875": {"name": "MUHAMMED ANAS VT", "unit": "SOUTH PANG"},
    "9446068970": {"name": "VM IRSHAD WAFY", "unit": "MATTATH KULAMBU"},
    "9048194199": {"name": "MUHAMMED NABEEL", "unit": "PANG KADANNAMUTTY"},
    "8921055575": {"name": "MOHAMMED FAIZ", "unit": "PANG KADANNAMUTTY"},
    "7356941375": {"name": "MISHAB KANAKKAYIL", "unit": "PANG KADANNAMUTTY"},
    "8590961354": {"name": "SHAHID AMEEN P", "unit": "PANG KADANNAMUTTY"},
    "9037800278": {"name": "SHAMHAN K", "unit": "PANG KADANNAMUTTY"}
}

# ==========================================
# 2. SESSION STATE & LOGIN LOGIC
# ==========================================
if 'user' not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.title("🔐 SKSSF Upload Portal")
    st.write("Enter your registered mobile number to access your unit's data.")
    
    mobile_input = st.text_input("Mobile Number", type="password", placeholder="10-digit number")
    
    if st.button("Login", width="stretch"):
        clean_number = mobile_input.strip()
        if clean_number in COORDINATORS:
            st.session_state.user = COORDINATORS[clean_number]
            st.rerun()
        else:
            st.error("Number not recognized. Contact Admin.")
    st.stop()

with st.sidebar:
    st.write(f"Logged in as: **{st.session_state.user['name']}**")
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

# ==========================================
# 3. DIRECT CLOUD CREDENTIALS & DATA LOADING
# ==========================================
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/16oELiftqVqKc3KEX0INOZ1rKBf6JEeJKC171tZEv9Uk/edit"

# Bypassing Streamlit Secrets to guarantee correct parsing of the JWT Signature
GCP_CREDS = {
  "type": "service_account",
  "project_id": "skssf-sprint",
  "private_key_id": "a340b2544b28811aa497bb854e7a65d815e7b2b4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCuTuvTE/1Zmi55\n01ZVQRdEnQjwoYLHw2II/+bvT+1QaopjomePB6b9bOSbJCUGYrHIVCySRRL/sFSy\ne4RVWTi8Vd6YNFtKysSDNC7Nntax9cnBrtU8f9dXLbYg7pVnYeu+PC05qO3YtmA2\nhUBH/dORWGkUAVc+k0iFkdeGP0pQIfiVQePfZ9jH21sp+vLmhipMzf5orH59s0a2\nTXDlwL8bxtoxO9r1P3koV6Dc+HRuijq3p4rpig9Uq+jrlF8oSdWkaj8ZQx5+4jso\nUFLHTmDgIxx1UuK9CP7s7CVBllabBl+w0E43Wuvnc5uCTO+OeFJ5fFikkVV3MypD\nysQhWokNAgMBAAECggEABATPzRsN4U37ulVUDT0l8zAHr7yZjk+D6B82TNgz6YG7\nVRa+en67q+Yh0y3fKKmH3c2LBYhQKtL+8OqGH42iED2Ol0XFwRCxvTCrz5PU8V9w\nWmXUhsOPzHPCWjoF+c85Jzat+EFb0n5J85fY5pAEm7pFGe/5+fhdWK8HIBI/fV9x\nWld1vEPoz73bWUSETdSzxYqHIU3fxIV+Nm5C7bf5QQ8ch2FThrgWfCUVATDb5AOr\nfnZ0Qok12mR9K/5Y3a7FSva5dCc2ivWhxU/xuYXV5BMgNXxN46OAV4qQ0Qk2Oou3\nol7YAeo4iuKsrjUuY55XD2K8fnuZvUuTVKcDpMqIYQKBgQDn1mDy1u0q/D1uhPnZ\nYkAQ++J2iDT2LNwrUqJSxVtA6g8cZ1eb2yriFAbFVFwN1W+gIwFpxHMd6pwQtNbK\nfOdtENyLUpJWa8xBKy066u3VfVZkJJeMQdkWYa3NwIfj71D7twAjPG+twCZAb/YA\nzofUEdAPB2XKzGHY6aYhW9J8qQKBgQDAeZ2qxMULCa6unTvLA64F9eN0QIedmKHI\njcZViBnD0nB7zKB+HrhjiPP83S0+oqqHPmu5oNvq38D3eb6e/9G5b81VxDSlJNiF\nbzU3IA1JfsB5L5tsLVryBkLbC3ihz84YkTKKEWnlBLPuUjxmvG1p83uDhRiHS+MA\nVCeiopmjxQKBgGe68NfWuHkyMR5hGxVbs4Sl3vbgDKpU+hHcQEq+iQzrbOVti7Jt\nhqtvAHSMQT/jTrWc1AYJ4uPw0/FZqH0jE70l/TfNMzK9ur8x3WPuN4n9MYlPIguc\nbtBn1gcobOTccCSgBcy+Ps3EGplcPvqvbfDCI5CF49KwTdtq920Xk385AoGAP+Fd\nMcsitpodDrkCmkt7W2ETf4bXO7fnof9j3wlPu81BJeVxMsqRWf+fMsJZfNtSC5bs\n++vmcVqX2crfODghbBEuLhPzgQfskMSq/cO2hTj7On1RcSLQd1kaoUZ6YAHvHfo6\nstY6thbMfQFwKIzLJ4n26VyoGmdWTMqhaPncUh0CgYAOatsaVudtI7aU1Bc39NMG\nveotcdlm/9mZiuQY9+lFVCS576gnuSYqATZZYCW/eNjSicCo2hBEYzHUSjifwDGK\noXaz6chc5yqe1+dM01v6fwBsRuWlFc7FPOy8n6mHkuNhHkuobyFndnszdwLvlDr/\nV3xlRC2A26juy2wEicplzg==\n-----END PRIVATE KEY-----\n",
  "client_email": "skssf-bot@skssf-sprint.iam.gserviceaccount.com",
  "client_id": "107017898940809833039",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/skssf-bot%40skssf-sprint.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

@st.cache_data(ttl=5)
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection, service_account_info=GCP_CREDS)
    df = conn.read(spreadsheet=SPREADSHEET_URL)
    
    if 'Reason_for_non_completion' not in df.columns:
        df['Reason_for_non_completion'] = ""
    if 'Last_Updated_By' not in df.columns:
        df['Last_Updated_By'] = ""
        
    df['Reason_for_non_completion'] = df['Reason_for_non_completion'].fillna("")
    df['Last_Updated_By'] = df['Last_Updated_By'].fillna("")
    return df

df = load_data()

# ==========================================
# 4. MAIN DASHBOARD & UNIT FILTERING
# ==========================================
is_admin = st.session_state.user['unit'] == "ALL"

if is_admin:
    st.title("⚡ Admin Control Center")
    unit_list = sorted(df['Unit_Name'].unique().tolist())
    selected_unit = st.selectbox("Select a Unit to view/edit:", unit_list)
else:
    selected_unit = st.session_state.user['unit']
    st.title(f"📍 {selected_unit} Portal")

unit_df = df[df['Unit_Name'] == selected_unit].copy()

total_count = len(unit_df)
done_count = len(unit_df[unit_df['2026_Uploaded'] == True])
pending_count = total_count - done_count

c1, c2, c3 = st.columns(3)
c1.metric("Total", total_count)
c2.metric("Done ✅", done_count)
c3.metric("Pending ⏳", pending_count)

st.progress(done_count / total_count if total_count > 0 else 0)
st.markdown("---")

# ==========================================
# 5. SPLIT LISTS & CLOUD SAVING
# ==========================================
st.subheader(f"⏳ Pending Members ({pending_count})")
st.caption("Tick the box ONLY after submitting in the SKSSF app.")

pending_df = unit_df[unit_df['2026_Uploaded'] == False].copy()

if pending_count > 0:
    col_config = {
        "2026_Uploaded": st.column_config.CheckboxColumn("Done?", default=False),
        "Name": st.column_config.TextColumn(disabled=True),
        "Father": st.column_config.TextColumn("Father/House", disabled=True),
        "Mobile": st.column_config.TextColumn("Phone", disabled=True),
        "Reason_for_non_completion": st.column_config.TextColumn("Reason if failed"),
        "Unit_Name": None,
        "House": None
    }
    
    if not is_admin:
        col_config["Last_Updated_By"] = None
    
    edited_pending = st.data_editor(
        pending_df,
        column_config=col_config,
        hide_index=True,
        width="stretch"
    )
    
    if st.button("💾 Save Updates", type="primary", width="stretch"):
        changes_made = False
        for index, row in edited_pending.iterrows():
            orig_row = pending_df.loc[index]
            
            if row['2026_Uploaded'] != orig_row['2026_Uploaded'] or row['Reason_for_non_completion'] != orig_row['Reason_for_non_completion']:
                df.at[index, '2026_Uploaded'] = row['2026_Uploaded']
                df.at[index, 'Reason_for_non_completion'] = row['Reason_for_non_completion']
                df.at[index, 'Last_Updated_By'] = st.session_state.user['name']
                changes_made = True
                
        if changes_made:
            conn = st.connection("gsheets", type=GSheetsConnection, service_account_info=GCP_CREDS)
            conn.update(spreadsheet=SPREADSHEET_URL, data=df)
            
            st.success("✅ Cloud Database Updated Successfully!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.info("No changes to save.")
else:
    st.success("🎉 All members in this unit are completed!")

st.markdown("---")

st.subheader(f"✅ Completed Members ({done_count})")
completed_df = unit_df[unit_df['2026_Uploaded'] == True]

if done_count > 0:
    st.dataframe(
        completed_df[['Name', 'Mobile', 'Reason_for_non_completion', 'Last_Updated_By'] if is_admin else ['Name', 'Mobile', 'Reason_for_non_completion']],
        hide_index=True,
        width="stretch"
    )
