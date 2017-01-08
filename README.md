# Cluster-Lab
Cluster:
+ mykmean.py: k-mean algorithm, 
gồm có các hàm đọc và ghi file csv, thuật toán kmean (truyền vào data, số k), và các độ đo eucliad, manhattan và cosine. 
trong đó độ đo cosine sử dụng angular distance tức là arccos của cosine simalarity để sử dụng như độ đo khoảng cách.
+ myplot.py: scatter plot
đọc input từ output của mykmean để visualize.
+ mydbscan.py: dbscan algorithm
thuật toán dbscan có 3 hàm chính là hàm region_query dùng để lấy hết tất cả các points nằm trong cluster, hàm expand_cluster dùng để mở rộng cluster với 1 điểm trung tâm, hàm dbscan thực hiện thuật toán dbscan với tham số eps và minpts.
+ reg_animal.py: 
xác định các động vật hay bị phân lớp sai bằng giả định chúng có nhiều liên kết yếu với nhiều động vật. chỉ cần chạy.
+ internal_evaluation.py: 
đo lường bằng độ đo Davies-bouldin để xác định độ tốt của thuật toán phân cụm