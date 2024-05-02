import PyPDF2
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io


def create_page_with_logo_and_blank(logo_path, page_size=letter):
    """Membuat PDF dengan logo yang disembunyikan oleh halaman kosong."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=page_size)
    
    can.drawImage(logo_path, 0, 0, width=page_size[0], height=page_size[1])
    
    can.setFillColorRGB(1, 1, 1)  
    can.rect(0, 0, page_size[0], page_size[1], fill=1, stroke=0)
    
    can.showPage()
    can.save()

    packet.seek(0)
    new_pdf = PyPDF2.PdfReader(packet)
    
    return new_pdf.pages[0]


def caesar_cipher(text, shift):
    """Mengubah teks berdasarkan pergeseran tertentu (Caesar cipher)."""
    result = []
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            new_char = chr(start + (ord(char) - start + shift) % 26)
            result.append(new_char)
        else:
            result.append(char)
    return ''.join(result)


def encode_metadata_base64(metadata):
    """Encode metadata dengan Base64."""
    encoded_metadata = {}
    for key, value in metadata.items():
        encoded_str = base64.b64encode(caesar_cipher(value, 4).encode()).decode()
        encoded_metadata[key] = encoded_str
    return encoded_metadata


def edit_pdf_with_modifications(input_pdf, output_pdf, new_metadata, logo_path):
    """Mengedit PDF dengan halaman tersembunyi di awal dan halaman kosong di akhir."""
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        hidden_logo_page = create_page_with_logo_and_blank(logo_path)
        pdf_writer.add_page(hidden_logo_page)

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        pdf_writer.add_page(create_page_with_logo_and_blank(logo_path))

        encrypted_metadata = encode_metadata_base64(new_metadata)

        pdf_writer.add_metadata(encrypted_metadata)

        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)


input_pdf = 'pdferica.pdf'
output_pdf = 'output1.pdf'
logo_path = 'telu.png'
new_metadata = {'/Title': 'Prototipe Sistem Monitoring Suhu, Ketinggian Air, dan Kontrol Otomatis pada Budidaya Ikan dalam EmberBerbasis IoT', '/Author': 'Erica', '/Subject': 'Forensika'}

edit_pdf_with_modifications(input_pdf, output_pdf, new_metadata, logo_path)