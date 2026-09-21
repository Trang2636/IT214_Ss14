#!/usr/bin/env python3
"""Generate the architecture dossier PDF from the approved Bai5 design content."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Ho_so_thiet_ke_Bai5_Saga_Combo.pdf"
FONT_DIR = Path("/System/Library/Fonts/Supplemental")

NAVY = colors.HexColor("#15304A")
BLUE = colors.HexColor("#1F6EAE")
CYAN = colors.HexColor("#27A7C4")
GREEN = colors.HexColor("#2B8A66")
ORANGE = colors.HexColor("#D77A22")
RED = colors.HexColor("#BE3A45")
INK = colors.HexColor("#243746")
MUTED = colors.HexColor("#607586")
PALE = colors.HexColor("#EEF5F9")
LINE = colors.HexColor("#C9D8E2")


def register_fonts():
    pdfmetrics.registerFont(TTFont("ArialVN", str(FONT_DIR / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("ArialVN-Bold", str(FONT_DIR / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("ArialVN-Italic", str(FONT_DIR / "Arial Italic.ttf")))
    pdfmetrics.registerFontFamily(
        "ArialVN", normal="ArialVN", bold="ArialVN-Bold", italic="ArialVN-Italic"
    )


class ArchitectureDiagram(Flowable):
    def __init__(self, width=170 * mm, height=78 * mm):
        super().__init__()
        self.width = width
        self.height = height

    def draw_box(self, canvas, x, y, w, h, title, subtitle, color):
        canvas.setFillColor(colors.white)
        canvas.setStrokeColor(color)
        canvas.setLineWidth(1.4)
        canvas.roundRect(x, y, w, h, 5, fill=1, stroke=1)
        canvas.setFillColor(color)
        canvas.roundRect(x, y + h - 11 * mm, w, 11 * mm, 5, fill=1, stroke=0)
        canvas.rect(x, y + h - 11 * mm, w, 5 * mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont("ArialVN-Bold", 9)
        canvas.drawCentredString(x + w / 2, y + h - 7 * mm, title)
        canvas.setFillColor(INK)
        canvas.setFont("ArialVN", 7.2)
        for index, line in enumerate(subtitle.split("\n")):
            canvas.drawCentredString(x + w / 2, y + h - 17 * mm - index * 4 * mm, line)

    def arrow(self, canvas, x1, y1, x2, y2, label):
        canvas.setStrokeColor(MUTED)
        canvas.setFillColor(MUTED)
        canvas.setLineWidth(1)
        canvas.line(x1, y1, x2, y2)
        canvas.line(x2, y2, x2 - 2.2 * mm, y2 + 1.4 * mm)
        canvas.line(x2, y2, x2 - 2.2 * mm, y2 - 1.4 * mm)
        canvas.setFont("ArialVN", 6.5)
        canvas.drawCentredString((x1 + x2) / 2, y1 + 2.2 * mm, label)

    def hotel_arrow(self, canvas, x1, y1, x2, y2):
        """Route above Flight so the Hotel connector never crosses another module."""
        top_y = 76 * mm
        canvas.setStrokeColor(MUTED)
        canvas.setFillColor(MUTED)
        canvas.setLineWidth(1)
        canvas.line(x1, y1, 55 * mm, top_y)
        canvas.line(55 * mm, top_y, x2, top_y)
        canvas.line(x2, top_y, x2, y2)
        canvas.line(x2, y2, x2 - 1.4 * mm, y2 + 2.2 * mm)
        canvas.line(x2, y2, x2 + 1.4 * mm, y2 + 2.2 * mm)
        canvas.setFont("ArialVN", 6.5)
        canvas.drawString(78 * mm, top_y - 3.2 * mm, "2. Hotel")

    def draw(self):
        c = self.canv
        c.setFillColor(PALE)
        c.roundRect(0, 0, self.width, self.height, 7, fill=1, stroke=0)
        box_w, box_h = 39 * mm, 29 * mm
        ox, oy = 8 * mm, 25 * mm
        self.draw_box(c, ox, oy, box_w, box_h, "COMBO ORDER", "Saga Orchestrator\nState + Trace", BLUE)

        positions = [
            (64 * mm, 45 * mm, "FLIGHT", "reserve / cancel\nPartner REST API", CYAN),
            (118 * mm, 45 * mm, "HOTEL", "reserve / cancel\nPartner REST API", GREEN),
            (91 * mm, 7 * mm, "PAYMENT", "charge / refund\nPayment Gateway", ORANGE),
        ]
        for x, y, title, subtitle, color in positions:
            self.draw_box(c, x, y, box_w, box_h, title, subtitle, color)

        self.arrow(c, ox + box_w, oy + 21 * mm, 64 * mm, 55 * mm, "1. Flight")
        self.hotel_arrow(c, ox + box_w, oy + 24 * mm, 118 * mm, 73 * mm)
        self.arrow(c, ox + box_w, oy + 7 * mm, 91 * mm, 21 * mm, "3. Payment")
        c.setFillColor(NAVY)
        c.setFont("ArialVN-Bold", 7)
        c.drawString(7 * mm, 8 * mm, "Nguyên tắc: mỗi service sở hữu dữ liệu riêng; sagaId là idempotency key xuyên suốt.")


def paragraph(text, style):
    return Paragraph(text, style)


def make_table(data, widths, header=True, font_size=8):
    table = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("FONTNAME", (0, 0), (-1, -1), "ArialVN"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]
    if header:
        commands += [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "ArialVN-Bold"),
        ]
    table.setStyle(TableStyle(commands))
    return table


def bullet_list(items, styles):
    result = []
    for item in items:
        result.append(Paragraph("• " + item, styles["BulletVN"]))
    return result


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    if doc.page == 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, height - 10 * mm, width, 10 * mm, fill=1, stroke=0)
    else:
        canvas.setStrokeColor(LINE)
        canvas.line(20 * mm, height - 14 * mm, width - 20 * mm, height - 14 * mm)
        canvas.setFont("ArialVN", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(20 * mm, height - 10.5 * mm, "BÀI TẬP 5 • SAGA COMBO BOOKING")
    canvas.setStrokeColor(LINE)
    canvas.line(20 * mm, 13 * mm, width - 20 * mm, 13 * mm)
    canvas.setFont("ArialVN", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 8.5 * mm, "Hồ sơ thiết kế kiến trúc")
    canvas.drawRightString(width - 20 * mm, 8.5 * mm, f"Trang {doc.page}")
    canvas.restoreState()


def build_pdf():
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitleVN", fontName="ArialVN-Bold", fontSize=25, leading=31,
        textColor=NAVY, alignment=TA_LEFT, spaceAfter=9 * mm,
    ))
    styles.add(ParagraphStyle(
        name="SubtitleVN", fontName="ArialVN", fontSize=12, leading=18,
        textColor=BLUE, spaceAfter=5 * mm,
    ))
    styles.add(ParagraphStyle(
        name="H1VN", fontName="ArialVN-Bold", fontSize=16, leading=20,
        textColor=NAVY, spaceBefore=3 * mm, spaceAfter=3 * mm,
    ))
    styles.add(ParagraphStyle(
        name="H2VN", fontName="ArialVN-Bold", fontSize=11.5, leading=15,
        textColor=BLUE, spaceBefore=3 * mm, spaceAfter=2 * mm,
    ))
    styles.add(ParagraphStyle(
        name="BodyVN", fontName="ArialVN", fontSize=9.2, leading=14,
        textColor=INK, alignment=TA_LEFT, spaceAfter=2.5 * mm,
    ))
    styles.add(ParagraphStyle(
        name="BulletVN", fontName="ArialVN", fontSize=8.8, leading=13,
        textColor=INK, leftIndent=4 * mm, firstLineIndent=-3 * mm, spaceAfter=1.3 * mm,
    ))
    styles.add(ParagraphStyle(
        name="CalloutVN", fontName="ArialVN-Bold", fontSize=9.2, leading=14,
        textColor=NAVY, backColor=PALE, borderColor=CYAN, borderWidth=0.8,
        borderPadding=8, spaceBefore=2 * mm, spaceAfter=4 * mm,
    ))
    styles.add(ParagraphStyle(
        name="SmallVN", fontName="ArialVN", fontSize=7.8, leading=11,
        textColor=MUTED, spaceAfter=1.5 * mm,
    ))

    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
        topMargin=20 * mm, bottomMargin=18 * mm, title="Hồ sơ thiết kế Bài 5 - Saga Combo Booking",
        author="Bài tập Microservices Session 14",
    )
    story = []

    story += [
        Spacer(1, 25 * mm),
        Paragraph("HỒ SƠ THIẾT KẾ<br/>KIẾN TRÚC HỆ THỐNG", styles["TitleVN"]),
        Paragraph('Bài tập 5 • Combo “Chuyến đi trọn gói”', styles["SubtitleVN"]),
        Spacer(1, 5 * mm),
        Table([
            ["Mô hình", "Saga Orchestration"],
            ["Phạm vi", "Flight + Hotel + Payment"],
            ["Công nghệ", "Java 21 • Spring Boot • OpenFeign • Eureka • REST mock"],
            ["Mục tiêu", "Toàn bộ thành công hoặc tự động bù trừ"],
        ], colWidths=[35 * mm, 125 * mm], style=TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "ArialVN-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "ArialVN"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 0), (0, -1), BLUE),
            ("TEXTCOLOR", (1, 0), (1, -1), INK),
            ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])),
        Spacer(1, 12 * mm),
        Paragraph(
            "Tài liệu trình bày phân tích nghiệp vụ, lựa chọn Saga, kiến trúc module, "
            "cơ chế compensate, timeout/retry và bốn kịch bản phục hồi bắt buộc.",
            styles["CalloutVN"],
        ),
        PageBreak(),
    ]

    story += [
        Paragraph("1. Bài toán và ràng buộc", styles["H1VN"]),
        Paragraph(
            "Khách hàng đặt vé máy bay và phòng khách sạn trong cùng một yêu cầu. Combo chỉ được "
            "xác nhận khi Flight, Hotel và Payment đều thành công. Ba hệ thống sở hữu API và dữ liệu "
            "riêng, nên không thể dùng một transaction database chung hoặc dựa vào ACID xuyên service.",
            styles["BodyVN"],
        ),
        Paragraph(
            "Giải pháp dùng chuỗi local transaction và compensating transaction để đạt eventual "
            "consistency. Đây là tính nguyên tử ở cấp nghiệp vụ, không phải rollback kỹ thuật tức thời.",
            styles["CalloutVN"],
        ),
        Paragraph("Các dịch vụ tham gia", styles["H2VN"]),
        make_table([
            ["Dịch vụ", "Trách nhiệm", "Dữ liệu sở hữu"],
            ["Combo Order", "Nhận yêu cầu, điều phối, lưu state/trace", "ComboOrder, sagaId"],
            ["Flight", "Giữ và hủy vé máy bay", "Flight reservation"],
            ["Hotel", "Giữ và hủy phòng", "Hotel reservation"],
            ["Payment", "Thu và hoàn tiền", "Payment transaction"],
            ["Eureka", "Service discovery (hạ tầng)", "Service registry"],
        ], [34 * mm, 78 * mm, 48 * mm]),
        Spacer(1, 4 * mm),
        Paragraph("Luồng giao dịch thuận", styles["H2VN"]),
    ]
    story += bullet_list([
        "Tạo ComboOrder PENDING và một sagaId duy nhất.",
        "Gọi Flight giữ chỗ; thành công chuyển FLIGHT_RESERVED.",
        "Gọi Hotel giữ phòng; thành công chuyển HOTEL_RESERVED.",
        "Gọi Payment thu tiền; thành công chuyển PAYMENT_COMPLETED.",
        "Xác nhận ComboOrder COMPLETED khi mọi bước đã hoàn tất.",
    ], styles)
    story += [
        Paragraph("Điểm có thể thất bại", styles["H2VN"]),
        make_table([
            ["Điểm lỗi", "Ví dụ", "Cách xử lý"],
            ["Flight", "Hết vé, 5xx, timeout", "Dừng Saga; chưa cần rollback bước trước"],
            ["Hotel", "Hết phòng, response chậm/mất", "Cancel Hotel an toàn + cancel Flight"],
            ["Payment", "Bị từ chối hoặc gateway lỗi", "Cancel Hotel rồi Flight"],
            ["Compensate", "Đối tác tạm unavailable", "Retry bền vững, DLQ, cảnh báo"],
            ["Orchestrator", "Restart giữa Saga", "Persist state + outbox trong production"],
        ], [34 * mm, 62 * mm, 64 * mm]),
        PageBreak(),
    ]

    story += [
        Paragraph("2. Lựa chọn Saga Orchestration", styles["H1VN"]),
        Paragraph(
            "Chọn Orchestration vì luồng combo có thứ tự rõ ràng, rollback phụ thuộc các bước đã "
            "hoàn thành và API của các đối tác không dùng chung một chuẩn sự kiện. Combo Order đóng "
            "vai trò điều phối trung tâm, giữ state machine và ra lệnh cho từng participant.",
            styles["BodyVN"],
        ),
        make_table([
            ["Tiêu chí", "Orchestration (chọn)", "Choreography"],
            ["Luồng nghiệp vụ", "Nhìn thấy tập trung, dễ kiểm soát", "Phân tán qua nhiều event"],
            ["Đối tác ngoài", "Adapter REST phù hợp API khác nhau", "Cần tích hợp event phức tạp"],
            ["Compensate", "Thứ tự ngược được xác định rõ", "Dễ khó theo dõi quan hệ event"],
            ["Quan sát/demo", "Một sagaId và trace xuyên suốt", "Cần distributed tracing đầy đủ"],
            ["Đánh đổi", "Orchestrator cần HA/persistence", "Coupling sự kiện và khó debug hơn"],
        ], [33 * mm, 64 * mm, 63 * mm]),
        Spacer(1, 6 * mm),
        Paragraph("3. Kiến trúc module", styles["H1VN"]),
        ArchitectureDiagram(),
        Paragraph(
            "Mỗi service chỉ cập nhật dữ liệu do mình sở hữu. Bản demo dùng ConcurrentHashMap; khi "
            "triển khai thực tế, mỗi service dùng database riêng và Combo Order persist Saga state.",
            styles["SmallVN"],
        ),
        PageBreak(),
    ]

    story += [
        Paragraph("4. Giao dịch thuận và cơ chế bù trừ", styles["H1VN"]),
        make_table([
            ["Bước thuận", "Trạng thái", "Compensate", "Idempotency"],
            ["Flight.reserve", "FLIGHT_RESERVED", "Flight.cancel", "Trả booking cũ / cancel lặp an toàn"],
            ["Hotel.reserve", "HOTEL_RESERVED", "Hotel.cancel", "Tombstone chặn request đến trễ"],
            ["Payment.charge", "PAYMENT_COMPLETED", "Payment.refund", "Một payment theo sagaId"],
            ["Xác nhận combo", "COMPLETED", "CANCELLED nếu rollback", "State theo sagaId"],
        ], [38 * mm, 38 * mm, 37 * mm, 47 * mm]),
        Spacer(1, 5 * mm),
        Paragraph("Thứ tự compensate", styles["H2VN"]),
        Paragraph(
            "Compensate chạy theo thứ tự ngược: <b>Payment → Hotel → Flight</b>. Với Payment bị "
            "từ chối, chưa có tiền bị capture nên chỉ hủy Hotel và Flight. Với Hotel lỗi/timeout, "
            "orchestrator vẫn gửi Hotel.cancel trước khi Flight.cancel.",
            styles["BodyVN"],
        ),
        Paragraph(
            "Điểm quan trọng của timeout: không nhận được response không đồng nghĩa đối tác chưa xử lý. "
            "Lệnh cancel Hotel luôn được gửi với cùng sagaId; tombstone cancelledSagas ngăn request cũ "
            "đến trễ tạo ghost booking.",
            styles["CalloutVN"],
        ),
        Paragraph("State machine", styles["H2VN"]),
        make_table([
            ["Luồng thành công", "PENDING → FLIGHT_RESERVED → HOTEL_RESERVED → PAYMENT_COMPLETED → COMPLETED"],
            ["Luồng lỗi", "Bất kỳ bước lỗi → COMPENSATING → CANCELLED"],
            ["Bù trừ lỗi", "COMPENSATING → COMPENSATION_FAILED → worker retry / DLQ"],
        ], [36 * mm, 124 * mm], header=False, font_size=8.5),
        Spacer(1, 6 * mm),
        Paragraph("Nguyên tắc participant", styles["H2VN"]),
    ]
    story += bullet_list([
        "Mỗi command mang sagaId làm idempotency key.",
        "Reserve/charge lặp lại trả kết quả cũ, không tạo giao dịch kép.",
        "Cancel/refund lặp lại vẫn trả trạng thái cuối hợp lệ.",
        "Không xóa dấu vết Saga; giữ audit log đủ lâu để reconciliation.",
    ], styles)
    story.append(PageBreak())

    story += [
        Paragraph("5. Luồng bốn kịch bản", styles["H1VN"]),
        Paragraph("Kịch bản 1 — Thành công toàn bộ", styles["H2VN"]),
        make_table([
            ["01", "Combo", "Tạo PENDING"],
            ["02", "Flight", "reserve → RESERVED"],
            ["03", "Hotel", "reserve → RESERVED"],
            ["04", "Payment", "charge → CAPTURED"],
            ["05", "Combo", "COMPLETED"],
        ], [13 * mm, 33 * mm, 114 * mm], header=False),
        Spacer(1, 5 * mm),
        Paragraph("Kịch bản 2 — Flight thành công, Hotel thất bại", styles["H2VN"]),
        make_table([
            ["01", "Flight", "reserve thành công"],
            ["02", "Hotel", "reserve trả lỗi nghiệp vụ HOTEL_FAILURE"],
            ["03", "Compensate", "Hotel.cancel idempotent → Flight.cancel"],
            ["04", "Combo", "CANCELLED"],
        ], [13 * mm, 33 * mm, 114 * mm], header=False),
        Spacer(1, 5 * mm),
        Paragraph("Kịch bản 3 — Payment thất bại", styles["H2VN"]),
        make_table([
            ["01", "Flight + Hotel", "Cả hai reserve thành công"],
            ["02", "Payment", "charge bị từ chối"],
            ["03", "Compensate", "Hotel.cancel → Flight.cancel"],
            ["04", "Combo", "CANCELLED"],
        ], [13 * mm, 33 * mm, 114 * mm], header=False),
        Spacer(1, 5 * mm),
        Paragraph("Kịch bản 4 — Hotel timeout", styles["H2VN"]),
        make_table([
            ["01", "Flight", "reserve thành công"],
            ["02", "Hotel", "Mỗi response chậm 5 giây; client timeout 2 giây"],
            ["03", "Retry", "Thử tối đa 3 lần với cùng sagaId"],
            ["04", "Compensate", "Hotel.cancel/tombstone → Flight.cancel"],
            ["05", "Combo", "CANCELLED; request Hotel đến trễ không tạo booking"],
        ], [13 * mm, 33 * mm, 114 * mm], header=False),
        PageBreak(),
    ]

    story += [
        Paragraph("6. Timeout, retry và phục hồi", styles["H1VN"]),
        Paragraph("Chính sách trong bản demo", styles["H2VN"]),
        make_table([
            ["Tham số", "Giá trị", "Ý nghĩa"],
            ["Connect timeout", "1 giây", "Không chờ lâu khi đối tác không kết nối được"],
            ["Read timeout Hotel", "2 giây", "Giới hạn thời gian đợi response"],
            ["Retry", "Tối đa 3 lần", "Cùng sagaId, backoff 200 ms đến 1 giây"],
            ["Mock timeout", "5 giây", "Buộc Feign phát sinh read timeout"],
            ["Sau retry", "Compensate", "Hủy Hotel an toàn rồi hủy Flight"],
        ], [42 * mm, 35 * mm, 83 * mm]),
        Spacer(1, 5 * mm),
        Paragraph("Quy tắc vận hành", styles["H2VN"]),
    ]
    story += bullet_list([
        "Chỉ retry lỗi tạm thời (connect/read timeout, 502/503/504); không retry hết phòng hoặc thanh toán bị từ chối.",
        "Dùng exponential backoff có jitter để tránh retry storm; deadline tổng phải nhỏ hơn timeout của client.",
        "Circuit breaker và bulkhead cô lập đối tác chậm, tránh làm cạn thread của Combo Order.",
        "Compensate thất bại phải được persist vào outbox, retry bởi worker và chuyển DLQ/cảnh báo khi quá ngưỡng.",
        "Reconciliation job đối chiếu định kỳ với đối tác để phát hiện booking/payment mồ côi.",
    ], styles)
    story += [
        Paragraph("Phân loại kết quả", styles["H2VN"]),
        make_table([
            ["Loại", "Ví dụ", "Quyết định"],
            ["Thành công chắc chắn", "HTTP 2xx + reservation ID", "Đi tiếp"],
            ["Thất bại chắc chắn", "HTTP 409 hết phòng", "Không retry; compensate"],
            ["Không chắc chắn", "Timeout / mất response", "Retry idempotent rồi cancel an toàn"],
            ["Bù trừ chưa xong", "Cancel trả 503", "COMPENSATION_FAILED + retry bền vững"],
        ], [39 * mm, 51 * mm, 70 * mm]),
        PageBreak(),
    ]

    story += [
        Paragraph("7. API và cấu trúc source", styles["H1VN"]),
        make_table([
            ["Service", "Port", "API chính"],
            ["Eureka", "8761", "Registry dashboard"],
            ["Combo Order", "8080", "POST /api/v1/combo-orders; GET /{sagaId}"],
            ["Flight", "8081", "POST/DELETE /api/v1/flights/reservations"],
            ["Hotel", "8082", "POST/DELETE /api/v1/hotels/reservations"],
            ["Payment", "8083", "POST /charges; POST /refunds/{sagaId}"],
        ], [38 * mm, 22 * mm, 100 * mm]),
        Spacer(1, 5 * mm),
        Paragraph("Input mô phỏng", styles["H2VN"]),
        make_table([
            ["scenario", "Kết quả mong đợi"],
            ["SUCCESS", "COMPLETED"],
            ["HOTEL_FAILURE", "CANCELLED; Flight đã rollback"],
            ["PAYMENT_FAILURE", "CANCELLED; Hotel và Flight đã rollback"],
            ["HOTEL_TIMEOUT", "CANCELLED sau retry; chống ghost booking"],
        ], [55 * mm, 105 * mm]),
        Spacer(1, 5 * mm),
        Paragraph("Cấu trúc nộp bài", styles["H2VN"]),
        Paragraph(
            "Mỗi service là một Gradle project độc lập, giống format project mẫu. File demo.http chứa "
            "bốn request; scripts/demo.sh chạy tuần tự; HO_SO_THIET_KE.md là bản hồ sơ có thể cập nhật; "
            "output/pdf chứa bản phát hành PDF.",
            styles["BodyVN"],
        ),
        Paragraph("Dữ liệu quan sát trong response", styles["H2VN"]),
    ]
    story += bullet_list([
        "sagaId và trạng thái cuối của ComboOrder.",
        "flightReservationId, hotelReservationId, paymentId nếu bước tương ứng thành công.",
        "failureReason cho lỗi gốc.",
        "trace có timestamp cho từng transition và từng compensate.",
    ], styles)
    story.append(PageBreak())

    story += [
        Paragraph("8. Production readiness và video demo", styles["H1VN"]),
        Paragraph("Nâng cấp cần có khi triển khai thực tế", styles["H2VN"]),
    ]
    story += bullet_list([
        "Persist Saga state và optimistic locking; không phụ thuộc bộ nhớ tiến trình.",
        "Transactional outbox/inbox và broker cho command/compensate bền vững.",
        "Circuit breaker, bulkhead, rate limit và deadline propagation.",
        "mTLS/OAuth2 giữa service; mã hóa dữ liệu nhạy cảm và audit trail.",
        "Distributed tracing theo sagaId; metric latency, retry, compensate và Saga bị treo.",
        "Reconciliation với Flight/Hotel/Payment và quy trình xử lý thủ công có kiểm soát.",
    ], styles)
    story += [
        Paragraph("Kịch bản quay video đề xuất", styles["H2VN"]),
        make_table([
            ["Bước", "Nội dung trình bày"],
            ["1", "Giới thiệu sơ đồ module, Saga Orchestration và state machine"],
            ["2", "Mở Eureka, xác nhận bốn service nghiệp vụ đã đăng ký"],
            ["3", "Chạy SUCCESS, chỉ ra COMPLETED và ba ID"],
            ["4", "Chạy HOTEL_FAILURE, chỉ ra Hotel/Flight compensate"],
            ["5", "Chạy PAYMENT_FAILURE, chỉ ra thứ tự Hotel → Flight"],
            ["6", "Chạy HOTEL_TIMEOUT, giải thích retry và tombstone"],
            ["7", "Kết luận eventual consistency và giới hạn của demo in-memory"],
        ], [18 * mm, 142 * mm]),
        Spacer(1, 7 * mm),
        Paragraph(
            "KẾT LUẬN — Thiết kế đáp ứng yêu cầu “hoặc thành công toàn bộ, hoặc hủy toàn bộ” ở cấp "
            "nghiệp vụ, có xử lý rõ kết quả không chắc chắn do timeout và có đường nâng cấp sang một "
            "Saga bền vững cho môi trường production.",
            styles["CalloutVN"],
        ),
    ]

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
