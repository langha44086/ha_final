import streamlit as st
import pandas as pd
import pickle

# Hàm lấy gợi ý sản phẩm
def get_recommendations(df, ma_san_pham, cosine_sim, nums=5):
    matching_indices = df.index[df['ma_san_pham'] == ma_san_pham].tolist()
    if not matching_indices:
        st.warning(f"Không tìm thấy sản phẩm với ID: {ma_san_pham}")
        return pd.DataFrame()
    idx = matching_indices[0]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:nums + 1]
    product_indices = [i[0] for i in sim_scores]

    return df.iloc[product_indices]

# Hiển thị sản phẩm gợi ý
def display_recommended_products(recommended_products, cols=5):
    for i in range(0, len(recommended_products), cols):

        col_list = st.columns(cols)
        for j, col in enumerate(col_list):
            if i + j < len(recommended_products):
                product = recommended_products.iloc[i + j]
                with col:
                    st.write(f"### {product['ten_san_pham']}")
                    gia_ban_formatted = f"{product['gia_ban']:,.0f}".replace(",", ".")
                    gia_goc_formatted = f"{product['gia_goc']:,.0f}".replace(",", ".")
                    st.write(f"**Giá bán:** {gia_ban_formatted} VND")
                    st.write(f"**Giá gốc:** {gia_goc_formatted} VND")
                    expander = st.expander("Mô tả")
                    product_description = product['mo_ta']
                    truncated_description = ' '.join(product_description.split()[:100]) + "..."
                    expander.write(truncated_description)

# Đọc dữ liệu sản phẩm ,khách hàng và tập đánh giá
df_products = pd.read_csv('San_pham_2xuly.csv')
df_customers = pd.read_csv('Khach_hang_2xuly.csv')

df_reviews = pd.read_csv('Danh_gia_final.csv')

# Đọc file cosine similarity
with open('products_cosine_sim.pkl', 'rb') as f:
    cosine_sim_new = pickle.load(f)

# Giới hạn danh sách sản phẩm và khách hàng
limited_products = df_products.head(20)
limited_customers = df_customers.head(20)

# Giao diện Streamlit
st.image('hasaki1.jpg', use_container_width=True)
st.title("💎 Hệ thống gợi ý sản phẩm Recommender System 💎")

# Tiêu đề
st.markdown('<p style="color:red; font-size:45px;"><b>Data Science Project 2 Deployment</b></p>', unsafe_allow_html=True)
st.write("Content-Based Filtering")

menu = ["Business Objective", "Hiển thị chart", "Gợi ý sản phẩm", "Gợi ý mã khách hàng", "Admin"]
choice = st.sidebar.selectbox('Menu', menu)

st.sidebar.write("""#### Thành viên thực hiện:
                 Phan Văn Minh & Cao Anh Hào""")
st.sidebar.write("""#### Giảng viên hướng dẫn: Ms Phương """)
st.sidebar.write("""#### Ngày báo cáo tốt nghiệp: 16/12/2024""")

if choice == 'Business Objective':
    st.subheader("Business Objective")
    st.write("""
    ###### HASAKI.VN là hệ thống cửa hàng mỹ phẩm chính hãng và dịch vụ chăm sóc sắc đẹp chuyên sâu với hệ thống cửa hàng trải dài toàn quốc. Họ muốn biết về sản phẩm của mình thông qua lựa chọn sản phẩm, đánh giá của khách hàng nhằm phục vụ tốt cho việc phát triển kinh doanh và đáp ứng thị hiếu của khách hàng.
    """)  
    st.write("""###### => Yêu cầu: Dùng thuật toán Machine Learning trong Python để giải quyết vấn đề. Cụ thể là dùng Content-based recommender system""")
    st.image("2.png")
    st.subheader("Thuật toán dùng trong Content-based")
    st.write("""Gensim""")
    st.image("1.png")
    st.write("""Cosine_similarity""")
    st.image("3.png")
    st.image("5.png")
    st.subheader("Thuật toán dùng trong Collaborative filtering")
    st.write("""Surprise""")
    st.image("6.png")
    
elif choice == 'Hiển thị chart':
    st.subheader("Dữ liệu đầu vào cho giao diện")
    st.image("4.png")
    st.subheader("Biểu đồ Heatmap")
    st.write("Lấy một phần nhỏ trong Cosine_sim,tương ứng với ma trận 18x18.Gồm các giá trị liên quan đến 18 sản phẩm đầu tiên trong danh sách để trực quan hoá")
    st.image('heatmap.png', use_container_width=True)

elif choice == 'Gợi ý sản phẩm':
    st.header("🔍 Gợi ý sản phẩm tương tự")

    product_options = [(row['ten_san_pham'], row['ma_san_pham']) for _, row in limited_products.iterrows()]
    selected_product = st.selectbox(
        "Chọn sản phẩm:",
        options=product_options,
        format_func=lambda x: x[0]
    )

    if selected_product:
        ma_san_pham = selected_product[1]
        selected_product_row = df_products[df_products['ma_san_pham'] == ma_san_pham].iloc[0]
        gia_ban_formatted = f"{selected_product_row['gia_ban']:,.0f}".replace(",", ".")
        gia_goc_formatted = f"{selected_product_row['gia_goc']:,.0f}".replace(",", ".")
        st.write("### Bạn đã chọn:")
        st.write(f"**Tên sản phẩm:** {selected_product_row['ten_san_pham']}")
        st.write(f"**Giá bán:** {gia_ban_formatted} VND")
        st.write(f"**Giá gốc:** {gia_goc_formatted} VND")

        recommendations = get_recommendations(df_products, ma_san_pham, cosine_sim_new, nums=5)
        if not recommendations.empty:
            st.write("### Các sản phẩm tương tự:")
            display_recommended_products(recommendations, cols=3)
        else:
            st.write("Không tìm thấy sản phẩm tương tự.")

elif choice == 'Gợi ý mã khách hàng':
    st.header("👤 Gợi ý sản phẩm theo mã khách hàng")

    customer_options = [(row['ho_ten'], row['userId']) for _, row in limited_customers.iterrows()]
    selected_customer = st.selectbox(
        "Chọn khách hàng:",
        options=customer_options,
        format_func=lambda x: x[0]
    )

    if selected_customer:
        user_id = selected_customer[1]
        customer_name = [cust[0] for cust in customer_options if cust[1] == user_id][0]
        st.write(f"Xin chào, **{customer_name}**!")

        recent_product = df_products.sample(1).iloc[0]  # Lấy sản phẩm ngẫu nhiên làm ví dụ

        st.write("### Sản phẩm gần nhất đã xem:")
        recent_gia_ban = f"{recent_product['gia_ban']:,.0f}".replace(",", ".")
        recent_gia_goc = f"{recent_product['gia_goc']:,.0f}".replace(",", ".")
        st.write(f"- **Tên sản phẩm:** {recent_product['ten_san_pham']}")
        st.write(f"- **Mã sản phẩm:** {recent_product['ma_san_pham']}")
        st.write(f"- **Giá bán:** {recent_gia_ban} VND")
        st.write(f"- **Giá gốc:** {recent_gia_goc} VND")

        recommendations = get_recommendations(df_products, recent_product['ma_san_pham'], cosine_sim_new, nums=5)
        if not recommendations.empty:
            st.write("### Các sản phẩm gợi ý:")
            display_recommended_products(recommendations, cols=3)
        else:
            st.write("Không tìm thấy sản phẩm gợi ý cho khách hàng này.")

elif choice == 'Admin':
    st.header("🔐 Đăng nhập quản lý")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        username = st.text_input("Tên đăng nhập:", key="admin_username")
        password = st.text_input("Mật khẩu:", type="password", key="admin_password")

        if st.button("Đăng nhập"):
            if username == "admin" and password == "admin":
                st.success("Đăng nhập thành công!")
                st.session_state["logged_in"] = True
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu.")
    else:
        st.subheader("Thông tin sản phẩm")
        st.markdown('<p style="color:green; font-size:30px;"><b>Nhóm sản phẩm được đánh giá 5 sao nhiều nhất</b></p>', unsafe_allow_html=True)
        top_rated_products = (df_reviews[df_reviews['so_sao'] == 5]
                              .groupby('ma_san_pham')
                              .size()
                              .reset_index(name='so_luong_5_sao')
                              .sort_values('so_luong_5_sao', ascending=False)
                              .head(5))

        if not top_rated_products.empty:
            st.write("### Top 5 sản phẩm được đánh giá 5 sao nhiều nhất:")
            for _, row in top_rated_products.iterrows():
                product_name = df_products[df_products['ma_san_pham'] == row['ma_san_pham']]['ten_san_pham'].values[0]
                st.write(f"- **{product_name}**: {row['so_luong_5_sao']} đánh giá 5 sao")
        else:
            st.write("Không có sản phẩm nào được đánh giá 5 sao.")

        product_options = [(row['ten_san_pham'], row['ma_san_pham']) for _, row in df_products.iterrows()]
        selected_product = st.selectbox(
            "Chọn sản phẩm:",
            options=product_options,
            format_func=lambda x: x[0],
            key="admin_product_selectbox"
        )

        if selected_product:
            ma_san_pham = selected_product[1]
            product_info = df_products[df_products['ma_san_pham'] == ma_san_pham].iloc[0]

            st.write(f"### {product_info['ten_san_pham']}")
            st.write(f"**Giá bán:** {product_info['gia_ban']:,} VND")
            st.write(f"**Giá gốc:** {product_info['gia_goc']:,} VND")
            st.write(f"**Phân loại:** {product_info['phan_loai']}")
            st.write(f"**Rating:** {product_info['rating']}")
            st.write(f"**Mô tả:** {product_info['mo_ta']}")

            # Lọc thông tin đánh giá liên quan đến sản phẩm
            product_reviews = df_reviews[df_reviews['ma_san_pham'] == ma_san_pham]

            if not product_reviews.empty:
                st.write("### Đánh giá từ khách hàng:")

                # Tính tổng số khen, chê và tổng số sao
                num_positive = product_reviews[product_reviews['sentiment'] == 0].shape[0]
                num_negative = product_reviews[product_reviews['sentiment'] == 1].shape[0]
                total_stars = product_reviews['so_sao'].sum()

                st.write(f"- **Tổng số khen:** {num_positive}")
                st.write(f"- **Tổng số chê:** {num_negative}")
                st.write(f"- **Tổng số sao:** {total_stars} ⭐")

                # Thống kê số lượng đánh giá theo số sao
                star_counts = product_reviews['so_sao'].value_counts().sort_index()
                st.write("- **Số lượng đánh giá theo số sao:**")
                for star, count in star_counts.items():
                    st.write(f"  - **{star} sao:** {count} đánh giá")

                # Hiển thị các đánh giá
                for _, review in product_reviews.iterrows():
                    st.write(f"- **Ngày bình luận:** {review['ngay_binh_luan']}")
                    st.write(f"- **Nội dung bình luận:** {review['content_new']}")
                    st.write(f"- **Số sao:** {review['so_sao']} ⭐")
                    st.markdown("---")
            else:
                st.write("Không có đánh giá nào cho sản phẩm này.")

        if st.button("Đăng xuất"):
            st.session_state["logged_in"] = False
            st.experimental_rerun()
