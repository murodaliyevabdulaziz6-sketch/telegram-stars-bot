import io
from datetime import datetime
from typing import List, Dict, Any
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def generate_users_excel(users: List[Dict[str, Any]]) -> io.BytesIO:
    """
    Generates a beautifully formatted Excel (.xlsx) file containing all users data.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Foydalanuvchilar"

    # Ensure gridlines are visible
    ws.views.sheetView[0].showGridLines = True

    # Styling definitions
    header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    
    title_font = Font(name="Calibri", size=16, bold=True, color="1F4E79")
    meta_font = Font(name="Calibri", size=10, italic=True, color="595959")
    
    data_font = Font(name="Calibri", size=10)
    bold_data_font = Font(name="Calibri", size=10, bold=True)
    
    zebra_fill = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    
    thin_border = Border(
        left=Side(style="thin", color="D9D9D9"),
        right=Side(style="thin", color="D9D9D9"),
        top=Side(style="thin", color="D9D9D9"),
        bottom=Side(style="thin", color="D9D9D9")
    )
    
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    # Title Block
    ws.merge_cells("A1:L1")
    ws["A1"] = "📊 TELEGRAM STARS BOT - FOYDALANUVCHILAR BAZASI"
    ws["A1"].font = title_font
    ws["A1"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[1].height = 25

    ws.merge_cells("A2:L2")
    ws["A2"] = f"Hisobot yaratilgan sana: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Jami foydalanuvchilar: {len(users)} ta"
    ws["A2"].font = meta_font
    ws["A2"].alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[2].height = 18

    # Headers
    headers = [
        ("№", 6, align_center),
        ("Telegram ID", 15, align_center),
        ("Username", 20, align_left),
        ("To'liq Ismi", 25, align_left),
        ("Stars Balansi (⭐)", 18, align_right),
        ("Sarflangan (⭐)", 16, align_right),
        ("Homiylik (⭐)", 16, align_right),
        ("Referallar (ta)", 15, align_center),
        ("Taklif qilgan ID", 16, align_center),
        ("VIP Maqomi", 16, align_center),
        ("Til", 8, align_center),
        ("Ro'yxatdan o'tgan sana", 22, align_center),
    ]

    header_row_idx = 4
    ws.row_dimensions[header_row_idx].height = 26

    for col_idx, (header_text, _, alignment) in enumerate(headers, start=1):
        cell = ws.cell(row=header_row_idx, column=col_idx, value=header_text)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = alignment
        cell.border = thin_border

    # Data Rows
    current_row = 5
    for i, u in enumerate(users, start=1):
        ws.row_dimensions[current_row].height = 20
        fill = zebra_fill if i % 2 == 0 else white_fill

        username_val = f"@{u['username']}" if u.get("username") else "-"
        full_name_val = u.get("full_name") or "-"
        balance_stars = u.get("balance_stars", 0) or 0
        total_spent = u.get("total_spent", 0) or 0
        total_donated = u.get("total_donated", 0) or 0
        ref_count = u.get("referrals_count", 0) or 0
        referrer_id_val = str(u.get("referrer_id")) if u.get("referrer_id") else "-"
        vip_level = u.get("vip_level", "Oddiy")
        lang = (u.get("lang") or "uz").upper()
        created_at = str(u.get("created_at") or "-")

        row_values = [
            (i, align_center, data_font),
            (u.get("user_id"), align_center, bold_data_font),
            (username_val, align_left, data_font),
            (full_name_val, align_left, data_font),
            (balance_stars, align_right, bold_data_font),
            (total_spent, align_right, data_font),
            (total_donated, align_right, data_font),
            (ref_count, align_center, bold_data_font),
            (referrer_id_val, align_center, data_font),
            (vip_level, align_center, data_font),
            (lang, align_center, data_font),
            (created_at, align_center, data_font),
        ]

        for col_idx, (val, alignment, font) in enumerate(row_values, start=1):
            cell = ws.cell(row=current_row, column=col_idx, value=val)
            cell.fill = fill
            cell.font = font
            cell.alignment = alignment
            cell.border = thin_border

        current_row += 1

    # Auto-adjust column widths
    for col_idx, (_, default_width, _) in enumerate(headers, start=1):
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = default_width

    # Save to in-memory bytes buffer
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output
