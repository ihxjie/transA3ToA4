# 将A3的PDF转为A4
# 将文件拖入窗口即可使用

import numpy as np
import PyPDF4
import tkinter, tkinter.filedialog
import windnd


def split_pdf(path, output_path):
    pdfWriter = PyPDF4.PdfFileWriter()
    writer = PyPDF4.PdfFileWriter()
    with open(path, 'rb') as infile:

        pdfReader = PyPDF4.PdfFileReader(infile)
        number_of_pages = pdfReader.getNumPages()

        for i in range(number_of_pages):

            page = pdfReader.getPage(i)
            width = float(page.mediaBox.getWidth())
            height = float(page.mediaBox.getHeight())

            pdfReader = PyPDF4.PdfFileReader(infile)

            page_top = pdfReader.getPage(i)
            page_top.mediaBox.lowerLeft = (0, height / 2)
            page_top.mediaBox.lowerRight = (width, height / 2)
            page_top.mediaBox.upperLeft = (0, height)
            page_top.mediaBox.upperRight = (width, height)
            pdfWriter.addPage(page_top)

            pdfReader = PyPDF4.PdfFileReader(infile)
            page_bottom = pdfReader.getPage(i)
            page_bottom.mediaBox.lowerLeft = (0, 0)
            page_bottom.mediaBox.lowerRight = (width, 0)
            page_bottom.mediaBox.upperLeft = (0, height / 2)
            page_bottom.mediaBox.upperRight = (width, height / 2)
            pdfWriter.addPage(page_bottom)

        number_list = get_list(pdfWriter.getNumPages())
        for i in range(pdfWriter.getNumPages()):
            writer.addPage(pdfWriter.getPage(number_list[i]))

        with open(output_path, 'wb') as output:
            writer.write(output)


def get_list(page_numbers):
    x1 = np.arange(page_numbers).reshape((int(page_numbers / 2), 2))
    x2 = []

    index = 1
    for i in range(len(x1)):
        if index == 1:
            x2.append(x1[i][1])
        else:
            x2.append(x1[i][0])

        index = 1 - index

    for i in range(len(x1) - 1, -1, -1):
        if index == 1:
            x2.append(x1[i][1])
        else:
            x2.append(x1[i][0])

        index = 1 - index

    return x2


def dragged_files(files):
    for item in files:
        print(item.decode('gbk'))
        path = item.decode('gbk')
        filename = path.split("\\")[-1]
        output_path = tkinter.filedialog.asksaveasfilename(initialfile=filename, filetypes=[('PDF', '*.pdf')])

        if output_path.find(".pdf") == -1 and output_path.find(".PDF") == -1:
            output_path += ".pdf"

        print(output_path)
        split_pdf(path, output_path)


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    tk = tkinter.Tk()
    tk.title('ihxjie')
    windnd.hook_dropfiles(tk, func=dragged_files)
    tk.mainloop()

