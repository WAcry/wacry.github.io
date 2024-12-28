---
title: "Phân tích sâu về định lý CAP: Xây dựng hệ thống phân tán có tính đồng thời và khả dụng cao"
date: 2024-12-27
draft: false
description: "Thảo luận về ứng dụng của định lý CAP trong hệ thống phân tán từ lý thuyết đến thực tiễn."
summary: "Thảo luận về ứng dụng của định lý CAP trong hệ thống phân tán từ lý thuyết đến thực tiễn."
tags: [ "Hệ thống phân tán", "Định lý CAP", "Thiết kế hệ thống", "Mô hình nhất quán" ]
categories: [ "Thiết kế hệ thống" , "Hệ thống phân tán" ]
---

## I. Định lý CAP

### 1.1 Định lý CAP là gì

**Định lý CAP** được Eric Brewer đưa ra vào năm 2000, quan điểm cốt lõi của nó là:

- **C (Consistency, Tính nhất quán)**: Tất cả các nút trong hệ thống đều nhìn thấy dữ liệu giống nhau tại cùng một thời điểm. Nói một cách chặt chẽ hơn, khi client đọc dữ liệu, bất kể đọc từ bản sao nào, kết quả phải nhất quán với dữ liệu đã được commit mới nhất (thường đề cập đến tính nhất quán mạnh/tính nhất quán tuyến tính).
- **A (Availability, Tính khả dụng)**: Hệ thống vẫn có thể cung cấp dịch vụ bình thường khi có một phần lỗi xảy ra, mỗi yêu cầu đều có thể nhận được "phản hồi hợp lệ" trong một khoảng thời gian hợp lý (không nhất thiết phải thành công, bao gồm cả phản hồi lỗi chính xác).
- **P (Partition tolerance, Tính chịu lỗi phân vùng)**: Hệ thống có thể chịu được phân vùng mạng (giao tiếp giữa các nút không thể truy cập được), ngay cả khi mạng bị chia cắt, hệ thống vẫn có thể cung cấp một mức độ khả dụng hoặc tính nhất quán nhất định.

Trong môi trường phân tán thực tế, phân vùng mạng là điều không thể tránh khỏi, vì vậy **P** về cơ bản được coi là "tùy chọn bắt buộc". Khi phân vùng mạng xảy ra, hệ thống không thể đồng thời đảm bảo **tính nhất quán mạnh** và **tính khả dụng cao** của dữ liệu trên tất cả các nút, mà chỉ có thể lựa chọn giữa C và A, do đó phát sinh hai loại chính là **CP** và **AP**.

### 1.2 Hạn chế của định lý CAP

Cần lưu ý rằng, bản thân định lý CAP là một lý thuyết tương đối ở cấp độ cao, được áp dụng để hướng dẫn khái niệm, **không thể hiểu đơn giản là "hoặc chọn C, hoặc chọn A"**. Có một số hiểu lầm phổ biến:

1. **C không nhất thiết là tính nhất quán mạnh**
   C trong định lý CAP thường đề cập đến tính nhất quán theo nghĩa chặt chẽ nhất (tức là tính nhất quán tuyến tính). Nhưng trong hệ thống thực tế, chúng ta có nhiều mô hình chi tiết hơn để lựa chọn như tính nhất quán yếu, đọc đã commit (Read Committed), tính nhất quán nhân quả (Causal Consistency), v.v.
2. **Tính khả dụng không phải là 0 hoặc 1**
   Không phải cứ chọn CP là tính khả dụng hoàn toàn bị hy sinh; hoặc chọn AP là tính nhất quán không được đảm bảo. Tính khả dụng và tính nhất quán đều có không gian thỏa hiệp và các chiến lược giảm cấp khác nhau.
3. **Tính nhất quán cuối cùng** không vi phạm CAP
   Đây là một giải pháp thỏa hiệp rất phổ biến, sử dụng tính nhất quán ghi thấp hơn để đổi lấy tính khả dụng và thông lượng cao hơn, đồng thời hội tụ dữ liệu ở chế độ nền thông qua phương thức không đồng bộ.

Do đó, định lý CAP nên được kết hợp với các **mô hình nhất quán**, **mô hình kiến trúc khả dụng cao** vào các tình huống cụ thể, thì mới có thể tạo ra giá trị hướng dẫn thực sự.

------

## II. Mô hình nhất quán của hệ thống phân tán

Việc phân loại các mô hình nhất quán rất phong phú, nhưng các mô hình chủ đạo phổ biến có thể được chia thành: **tính nhất quán mạnh** và **tính nhất quán yếu** (trong đó bao gồm tính nhất quán cuối cùng, tính nhất quán nhân quả, v.v.). Bài viết này chủ yếu giới thiệu **tính nhất quán mạnh** và **tính nhất quán cuối cùng**, đồng thời giải thích các ứng dụng phổ biến của chúng trong chế độ CP hoặc AP.

### 2.1 Tính nhất quán mạnh

**Tính nhất quán mạnh (Strong Consistency)** còn được gọi là **tính nhất quán tuyến tính (Linearizability)**, đề cập đến việc một khi thao tác ghi hoàn thành và trả về thành công, bất kỳ thao tác đọc nào sau đó đều có thể đọc được nội dung cập nhật đó. Nói cách khác, hệ thống thể hiện ra bên ngoài như thể đã thực hiện tất cả các thao tác một cách tuần tự.

- **Triển khai phổ biến**: Dựa vào sao chép đồng bộ và cơ chế trọng tài (đa số), thông qua các giao thức (như Paxos/Raft) để đảm bảo rằng chỉ có một leader (người lãnh đạo) hợp lệ trong hệ thống, tất cả các thao tác được ghi vào nhật ký theo thứ tự và sao chép đến đa số các nút.
- Ưu nhược điểm:
    - Ưu điểm: Đảm bảo tính chính xác dữ liệu nghiêm ngặt nhất, dữ liệu đọc được không bao giờ bị "quay lại".
    - Nhược điểm: Khi mạng bị rung lắc, phân vùng hoặc leader bị lỗi, để duy trì tính nhất quán, thao tác ghi thường bị chặn, dẫn đến giảm tính khả dụng tổng thể; hiệu suất và thông lượng cũng tương đối thấp hơn.

### 2.2 Tính nhất quán cuối cùng

**Tính nhất quán cuối cùng (Eventual Consistency)** là một hình thức điển hình của tính nhất quán yếu, nó chỉ yêu cầu nếu hệ thống không còn thao tác cập nhật mới, theo thời gian, dữ liệu của tất cả các bản sao sẽ dần hội tụ về cùng một trạng thái. Trong thời gian đó, người dùng đọc dữ liệu bản sao có thể thấy các giá trị đã lỗi thời, nhưng cuối cùng sẽ trở nên nhất quán.

- **Triển khai phổ biến**: Giao thức Gossip, sao chép không đồng bộ nhiều bản sao, CRDT (Conflict-free Replicated Data Type), v.v.
- Ưu nhược điểm:
    - Ưu điểm: Tính khả dụng cao, thông lượng cao, độ trễ thao tác ghi thấp, khả năng chịu lỗi phân vùng mạng cao.
    - Nhược điểm: Cần chấp nhận sự không nhất quán dữ liệu trong thời gian ngắn, logic ứng dụng phức tạp hơn, có thể phải thực hiện phát hiện và hợp nhất xung đột.

------

## III. Các giao thức và thuật toán nhất quán phổ biến

Để các bản sao của hệ thống phân tán duy trì tính nhất quán, ngành công nghiệp đã đưa ra nhiều thuật toán và giao thức cổ điển. Dưới đây là giới thiệu ngắn gọn về một số loại:

### 3.1 Paxos

Paxos là một thuật toán nhất quán phân tán do Leslie Lamport đề xuất vào những năm 1990, chủ yếu được sử dụng để thực hiện tính nhất quán mạnh hoặc tính nhất quán tuyến tính.

- **Nguyên tắc cơ bản**: Thông qua việc phân chia vai trò (Proposer - Người đề xuất, Acceptor - Người chấp nhận, Learner - Người học) để thực hiện nhiều vòng bỏ phiếu, để quyết định xem một thao tác hoặc giá trị có được đa số các nút chấp nhận hay không.
- Ưu nhược điểm:
    - Ưu điểm: Có thể đạt được sự nhất quán ngay cả khi có phân vùng mạng, lỗi nút, có tính bảo mật cao.
    - Nhược điểm: Triển khai phức tạp, khó gỡ lỗi và khắc phục sự cố, nhiều vòng bỏ phiếu dẫn đến hiệu suất bị hạn chế. Ngành công nghiệp thường sử dụng các biến thể của nó (Multi-Paxos, v.v.).

### 3.2 Raft

Raft được chính thức đề xuất vào năm 2013, mục tiêu là **đơn giản hóa việc triển khai và độ khó hiểu trong khi vẫn đảm bảo tính bảo mật tương đương với Paxos**. Nó thiết lập một vai trò **leader (người lãnh đạo)** ổn định, tập trung vào việc sao chép nhật ký và khôi phục lỗi:

- **Các giai đoạn quan trọng**: Bầu chọn leader (Leader Election), sao chép nhật ký (Log Replication), tính bảo mật (Safety), v.v.
- **Ứng dụng phổ biến**: Etcd, Consul, TiKV, LogCabin, v.v. đều dựa trên Raft để thực hiện sao chép nhất quán mạnh.
- Ưu nhược điểm:
    - Ưu điểm: Tương đối dễ hiểu, lượng code triển khai ít hơn; hiệu suất tốt hơn cho các cụm nhỏ và vừa.
    - Nhược điểm: Phụ thuộc vào nút chính (Leader), lỗi hoặc phân vùng của nút chính sẽ gây ra tắc nghẽn ghi tạm thời; khi triển khai trên các cụm lớn hoặc trên nhiều khu vực địa lý, độ trễ và tính khả dụng sẽ bị ảnh hưởng.

### 3.3 Giao thức Gossip

Giao thức Gossip (tám chuyện) không phải là một giao thức đồng thuận truyền thống, nó chủ yếu được sử dụng trong các tình huống phi tập trung để trao đổi siêu dữ liệu hoặc thông tin trạng thái thông qua tương tác ngẫu nhiên giữa các nút, do đó khuếch tán và hội tụ trên toàn mạng.

- **Đặc điểm**: Phi tập trung, chi phí thấp, các nút trao đổi tin nhắn định kỳ và ngẫu nhiên.
- **Ứng dụng phổ biến**: Cassandra, Riak, quản lý thành viên phân tán (như Serf), v.v., được sử dụng để thực hiện tính nhất quán cuối cùng, đồng bộ trạng thái bản sao, v.v.
- Ưu nhược điểm:
    - Ưu điểm: Khả năng mở rộng tốt, dễ triển khai, phù hợp với các tình huống không yêu cầu cao về tính nhất quán, yêu cầu cao về khả năng mở rộng.
    - Nhược điểm: Đảm bảo tính nhất quán yếu, cần các biện pháp xử lý xung đột ở cấp độ cao hơn (như CRDT, hợp nhất số phiên bản, v.v.) để giải quyết xung đột cuối cùng.

### 3.4 2PC / 3PC

Trong các tình huống giao dịch phân tán, các giao thức commit phổ biến là **2PC (Two-phase Commit)** và **3PC (Three-phase Commit)**:

- **2PC**: Điều phối viên thông báo cho tất cả những người tham gia "chuẩn bị commit (prepare)", nếu tất cả đều thành công thì phát "commit", nếu không thì "rollback (hủy bỏ)".
- **3PC**: Thêm một giai đoạn trên cơ sở 2PC, giảm tắc nghẽn do lỗi một điểm, nhưng việc triển khai phức tạp hơn, vẫn có vấn đề không khả dụng trong các tình huống phân vùng mạng hoặc lỗi nghiêm trọng.
- Ưu nhược điểm:
    - Ưu điểm: Dễ hiểu, ngữ nghĩa giao dịch rõ ràng, được ứng dụng rộng rãi trong cơ sở dữ liệu phân tán, hàng đợi tin nhắn, v.v.
    - Nhược điểm: Phụ thuộc nhiều vào điều phối viên, có nguy cơ bị tắc nghẽn; khi mạng bị phân vùng trong thời gian dài, có thể không thể tiếp tục giao dịch.

------

## IV. Hai lựa chọn chủ đạo của CAP: CP và AP

Khi chúng ta xác định **P** là thuộc tính "bắt buộc", thì hệ thống phân tán nếu muốn tiếp tục cung cấp dịch vụ khi có phân vùng mạng, thì phải lựa chọn giữa **C** và **A**. Do đó, thiết kế hệ thống phổ biến được chia thành hai phe chính là **CP** và **AP**.

### 4.1 Hệ thống CP

**CP (Consistency + Partition tolerance)**: Khi gặp phân vùng mạng, hệ thống sẽ chọn **ưu tiên đảm bảo tính nhất quán**, **hy sinh tính khả dụng** khi cần thiết.

- Triển khai điển hình:
    - Đồng thuận đa số (Paxos, Raft, v.v.), cần hơn một nửa số nút hoạt động và đạt được sự nhất quán thì mới cho phép ghi.
    - Nếu không thể đạt được quorum (số đại biểu tối thiểu) hoặc nút chính bị lỗi, hệ thống sẽ chặn hoặc từ chối thao tác ghi, để tránh tình trạng chia não dẫn đến dữ liệu không nhất quán.
- Ứng dụng phổ biến:
    - Zookeeper, Etcd, Consul, dịch vụ khóa phân tán, quản lý siêu dữ liệu phân tán, v.v.
    - Các tình huống yêu cầu tính nhất quán cao như quy trình cốt lõi của giao dịch tài chính, hệ thống kế toán ngân hàng, v.v.
- Đặc điểm:
    - Có đảm bảo dữ liệu nghiêm ngặt: Thà ngừng hoạt động chứ không để xảy ra tình trạng hai nút chính hoặc dữ liệu hỗn loạn.
    - Hy sinh một phần tính khả dụng: Khi xảy ra phân vùng mạng hoặc chuyển đổi dự phòng, sẽ có một khoảng thời gian dịch vụ không khả dụng hoặc từ chối thao tác ghi.

### 4.2 Hệ thống AP

**AP (Availability + Partition tolerance)**: Khi gặp phân vùng mạng, hệ thống sẽ chọn **ưu tiên đảm bảo tính khả dụng**, đồng thời **nới lỏng tính nhất quán**.

- Triển khai điển hình:
    - Tính nhất quán cuối cùng, sao chép nhiều nút chính, giao thức Gossip, chiến lược nhất quán có thể điều chỉnh theo phong cách Dynamo, v.v.
- Ứng dụng phổ biến:
    - Cơ sở dữ liệu NoSQL (Cassandra, Riak, DynamoDB, v.v.), hệ thống bộ nhớ đệm phân tán (Redis Cluster), v.v.
    - Các nghiệp vụ yêu cầu tính khả dụng cao, thông lượng cao, yêu cầu về tính nhất quán dữ liệu tương đối lỏng lẻo như mạng xã hội, thu thập nhật ký, hệ thống đề xuất, v.v.
- Đặc điểm:
    - Ngay cả khi có phân vùng, tất cả các nút vẫn nhận yêu cầu đọc và ghi, đảm bảo hệ thống "khả dụng nhất có thể".
    - Dữ liệu có thể không nhất quán trong thời gian ngắn, nhưng sẽ dần hội tụ ở chế độ nền thông qua đồng bộ không đồng bộ, hợp nhất xung đột, v.v.

------

## V. Làm thế nào để lựa chọn giữa CP và AP?

Trong các hệ thống phân tán quy mô lớn thực tế, thường **rất ít khi chỉ dựa vào một mô hình duy nhất**, mà là xử lý phân lớp cho các dữ liệu hoặc tình huống nghiệp vụ khác nhau, để đạt được sự cân bằng tối ưu giữa **tính nhất quán** và **tính khả dụng**.

1. **Dữ liệu cốt lõi chọn CP**
    - Ví dụ như số dư tài khoản người dùng, thanh toán đơn hàng, dòng tiền giao dịch tài chính, v.v., yêu cầu tính nhất quán rất cao.
    - Chấp nhận việc không thể ghi tạm thời do mạng bị rung lắc, nhưng không thể chấp nhận lỗi về số dư hoặc số tiền giao dịch.
2. **Dữ liệu biên hoặc dữ liệu bộ nhớ đệm chọn AP**
    - Ví dụ như bộ nhớ đệm của trang chi tiết sản phẩm, nhật ký hành vi người dùng, danh sách ứng viên đề xuất, v.v., yêu cầu về tính nhất quán thấp hơn.
    - Coi trọng tính đồng thời cao, tính khả dụng cao hơn, có thể chấp nhận việc cập nhật chậm trễ hoặc đọc dữ liệu bẩn trong một khoảng thời gian nhất định.

Nhiều doanh nghiệp internet sẽ sử dụng **kiến trúc hỗn hợp**: quy trình giao dịch cốt lõi sử dụng bộ nhớ kiểu CP (như cơ sở dữ liệu quan hệ phân tán hoặc bộ nhớ phân tán có tính nhất quán mạnh); các nghiệp vụ ngoại vi hoặc các tình huống "đọc nhiều ghi ít" sử dụng bộ nhớ kiểu AP hoặc giải pháp bộ nhớ đệm.

------

## VI. CP và AP làm thế nào để đạt được tính đồng thời cao và tính nhất quán cuối cùng

### 6.1 Hệ thống CP làm thế nào để đối phó với tính đồng thời cao

Mặc dù các giao thức đồng thuận sẽ phải đối mặt với độ trễ cao hơn và thông lượng thấp hơn khi quy mô nút cụm đơn lẻ và lượng yêu cầu ghi lớn, nhưng vẫn có thể cải thiện tính đồng thời và khả năng mở rộng thông qua các phương tiện sau:

1. Đọc và ghi hàng loạt
    - Đóng gói nhiều thao tác ghi ở client hoặc lớp trung gian, ghi một lần vào nút leader, giảm số lần khứ hồi mạng và số vòng giao thức.
2. Phân tách cơ sở dữ liệu và bảng & Nhiều cụm
    - Chia dữ liệu theo logic hoặc hash thành nhiều cụm (sharding), mỗi cụm vẫn chạy giao thức CP; các yêu cầu được phân tán đến các phân đoạn khác nhau thông qua lớp định tuyến hoặc proxy.
    - Cải thiện khả năng đồng thời tổng thể và giới hạn ảnh hưởng của lỗi trong một phân đoạn duy nhất.

> Thông lượng của cụm phân đoạn đơn của hệ thống CP thường thấp hơn 2 đến 10 lần so với hệ thống AP.

### 6.2 Hệ thống AP làm thế nào để đảm bảo tính nhất quán cuối cùng

Hệ thống AP thường có thể cung cấp thông lượng ghi và tính khả dụng đọc rất cao, nhưng lại nới lỏng tính nhất quán, do đó cần phải thực hiện đảm bảo hội tụ tính nhất quán ở lớp nền hoặc lớp logic nghiệp vụ:

1. Số phiên bản (Vector Clock) hoặc dấu thời gian logic
    - Gán một số phiên bản cho mỗi thao tác cập nhật (hoặc dựa trên Lamport Clock / Hybrid Clock), trong các tình huống xung đột, thực hiện hợp nhất hoặc chiến lược thắng dựa trên dấu thời gian (Last Write Wins).
2. Giao thức Gossip / Cơ chế chống entropy (Anti-entropy)
    - Các nút định kỳ trao đổi dữ liệu hoặc siêu dữ liệu mới nhất, nếu phát hiện xung đột thì thực hiện hợp nhất.
3. Chiến lược nhất quán có thể điều chỉnh
    - Lấy mô hình Dynamo làm đại diện, client có thể cấu hình các tham số `R`, `W` (như ghi đa số, xác nhận bản sao), do đó điều chỉnh linh hoạt giữa tính nhất quán và tính khả dụng.
4. Chiến lược giải quyết xung đột tùy chỉnh
    - Kết hợp ngữ nghĩa nghiệp vụ để hợp nhất, ví dụ như giỏ hàng sử dụng hợp nhất "hợp", bộ đếm sử dụng CRDT (G-counter, PN-counter, v.v.) để đảm bảo tính đơn điệu của dữ liệu.

------

## VII. Thực hiện tính nhất quán mạnh trên nhiều phân đoạn của CP

Như đã đề cập trong chương VII, **thông qua phân tách cơ sở dữ liệu và bảng (Sharding)** có thể "tách" áp lực của một cụm CP duy nhất thành nhiều cụm con, để hỗ trợ tính đồng thời cao hơn. Tuy nhiên, khi nghiệp vụ cần thực hiện giao dịch trên nhiều phân đoạn (tức là liên quan đến việc cập nhật nhiều cơ sở dữ liệu hoặc bảng), vẫn phải đối mặt với thách thức về **tính nhất quán trên nhiều phân đoạn**. Thông thường có các ý tưởng sau:

1. **Giao dịch phân tán: 2PC / 3PC**
    - Nếu ứng dụng cần thực hiện cập nhật nguyên tử trên nhiều phân đoạn, thường sử dụng giao thức giao dịch phân tán (như 2PC, 3PC) để điều phối việc commit hoặc rollback của các phân đoạn.
    - Vấn đề và đối sách:
        - 2PC/3PC đều phụ thuộc vào một nút điều phối viên, có thể trở thành nút thắt cổ chai.
        - Trong trường hợp phân vùng mạng nghiêm trọng hoặc điều phối viên bị lỗi, có thể xảy ra tắc nghẽn.
        - Thông thường sẽ giảm ảnh hưởng của tắc nghẽn và rủi ro không nhất quán dữ liệu thông qua chuyển đổi chính-phụ, phát hiện nhịp tim và cơ chế hết thời gian chờ, thử lại lũy đẳng, MVCC, v.v.
2. **Kiến trúc dựa trên ô (Cell-based)**
    - Chia nghiệp vụ thành nhiều ô tự trị, dữ liệu trong mỗi ô đều nằm trong cùng một tập hợp phân đoạn, đảm bảo rằng hầu hết các giao dịch chỉ được hoàn thành trong một ô duy nhất, giảm thao tác trên nhiều phân đoạn.
    - Sử dụng cơ chế không đồng bộ hoặc tính nhất quán cuối cùng trên ranh giới ô để trao đổi dữ liệu, đồng thời xem xét tính khả dụng và tính nhất quán tổng thể.
3. **Cơ sở dữ liệu phân tán toàn cầu + Giao thức đồng thuận toàn cục**
    - Ví dụ như Google Spanner thực hiện sao chép nhất quán mạnh trên mỗi phân đoạn (Shard) thông qua Paxos, sau đó sử dụng TrueTime API để cung cấp dấu thời gian toàn cục để đảm bảo tính nhất quán trên nhiều phân đoạn.
    - Giải pháp này có độ phức tạp triển khai rất cao, nhưng có thể cung cấp khả năng giao dịch phân tán gần như nhất quán mạnh trong phạm vi toàn cầu.

> **Tóm tắt**: Đối với các giao dịch trên nhiều phân đoạn yêu cầu nghiêm ngặt tính nhất quán mạnh, **2PC/3PC + điều phối viên** vẫn là giải pháp phổ biến, đồng thời cố gắng tăng tính khả dụng cao của điều phối viên để giảm khả năng xảy ra lỗi. Nhưng cần cố gắng giảm thiểu thao tác ghi trên nhiều phân đoạn trong thực tiễn kỹ thuật, hoặc giảm độ phức tạp của hệ thống thông qua ý tưởng ô để giới hạn hầu hết các giao dịch trong phạm vi một phân đoạn duy nhất.

------

## VIII. Thảo luận về các trường hợp nổi tiếng

Dưới đây là thảo luận ngắn gọn về một số hệ thống phân tán thường được đề cập trong ngành, hãy xem cách chúng lựa chọn và thực hiện CAP:

1. **Google Spanner**
    - Một hệ thống **CP** điển hình (thậm chí có thể đạt được ảo giác "CA" mà bên ngoài thường nói, nhưng về bản chất vẫn cần phải hy sinh một phần tính khả dụng).
    - Sử dụng dấu thời gian chính xác bên ngoài do TrueTime cung cấp + sao chép Paxos bên trong mỗi phân đoạn, đảm bảo tính nhất quán mạnh trên các trung tâm dữ liệu.
    - Phù hợp với các tình huống giao dịch tài chính toàn cầu hoặc yêu cầu tính nhất quán cao, nhưng chi phí cơ sở hạ tầng rất cao.
2. **BigTable / HBase**
    - Bề ngoài thiên về **CP** hơn, đảm bảo tính nhất quán của siêu dữ liệu thông qua điều phối phân tán giữa RegionServer và Master.
    - Nhưng trong đường dẫn đọc và ghi thực tế, cũng có thể cung cấp một số phương tiện khả dụng cao thông qua sao chép không đồng bộ nhiều bản sao, tính nhất quán khi đọc có thể được điều chỉnh theo nhu cầu của ứng dụng.
3. **AWS DynamoDB**
    - Thiên về **AP**, cảm hứng thiết kế ban đầu đến từ bài báo Dynamo, có thể điều chỉnh cấp độ nhất quán thông qua các tham số `R`, `W`, v.v.
    - Ở chế độ mặc định, cung cấp tính khả dụng cực cao và tính nhất quán cuối cùng, cũng có thể bật "đọc nhất quán mạnh" (nhưng chỉ đảm bảo tính nhất quán mạnh của một phân vùng, không nhất thiết phải trên nhiều phân vùng).
4. **Cassandra**
    - Cũng có xu hướng **AP**, lớp dưới sử dụng giao thức Gossip để duy trì trạng thái topo của nút.
    - Tính nhất quán khi đọc và ghi có thể cấu hình số lượng bản sao đọc và ghi `R` / `W`, để thực hiện chuyển đổi mượt mà từ tính nhất quán cuối cùng sang tính nhất quán mạnh hơn.

> **So sánh có thể thấy**: Về mặt kỹ thuật, không có "AP hoặc CP" tuyệt đối, mà là sự kết hợp của nhiều chiến lược nhất quán; hầu hết các hệ thống đều cung cấp một mức độ nhất quán có thể điều chỉnh để phù hợp với các tình huống ứng dụng khác nhau.

------

## IX. Tổng kết

1. **Định lý CAP không phải là một kích thước phù hợp cho tất cả**
    - Các hệ thống phân tán thực tế không thể nói đơn giản là "tôi chọn C, từ bỏ A" hoặc "tôi chọn A, từ bỏ C".
    - Trong ngành, phổ biến hơn là linh hoạt lựa chọn chế độ **CP** hoặc **AP** cho các chiều dữ liệu khác nhau, các loại thao tác khác nhau, thậm chí trong cùng một hệ thống, sử dụng các chiến lược chịu lỗi và nhất quán khác nhau cho các bảng/chức năng khác nhau.
2. **AP không phải là khả dụng 100% tuyệt đối**
    - Ví dụ, Cassandra, DynamoDB, v.v. cũng sẽ xuất hiện tình huống không thể đáp ứng yêu cầu khi có phân vùng mạng nghiêm trọng hoặc các nút bị lỗi trên diện rộng.
    - Hệ thống AP chỉ có thiết kế thiên về "chỉ cần bản sao có thể ghi thì cứ ghi trước", hy sinh một phần đảm bảo tính nhất quán để đổi lấy tính khả dụng và thông lượng tương đối cao hơn.
3. **CP cũng có thể cố gắng đạt được tính khả dụng cao**
    - Paxos/Raft cũng có thể cung cấp tính khả dụng 99,99% hoặc thậm chí cao hơn trong điều kiện bình thường, chỉ là cần đầu tư nhiều chi phí mạng, phần cứng và kỹ thuật hơn, và vẫn sẽ xuất hiện tình trạng chặn ghi, hy sinh tính khả dụng để duy trì tính nhất quán khi có phân vùng mạng nghiêm trọng.
4. **Kiến trúc hỗn hợp là chủ đạo**
    - Các tình huống giao dịch cốt lõi kiên trì tính nhất quán mạnh (CP), các tình huống hỗ trợ ngoại vi hoặc kênh bộ nhớ đệm sử dụng tính nhất quán yếu (AP), cả hai phối hợp với nhau.
    - Cần kết hợp khả năng chấp nhận của nghiệp vụ, môi trường mạng, chi phí đầu tư, dự trữ kỹ thuật của nhóm để đưa ra lựa chọn toàn diện.

Định lý CAP cung cấp một khung tư duy ở cấp độ cao cho việc thiết kế hệ thống phân tán, giúp chúng ta đưa ra quyết định hợp lý trước thực tế không thể tránh khỏi của phân vùng mạng. Trong hệ thống thực tế, cần phải sử dụng các **mô hình nhất quán**, **giao thức đồng thuận**, **cơ chế sao chép nhiều bản sao** phong phú hơn, cũng như thực tiễn kỹ thuật (khắc phục thảm họa, giảm cấp, lũy đẳng, hợp nhất xung đột, v.v.) để cân bằng tính nhất quán và tính khả dụng.