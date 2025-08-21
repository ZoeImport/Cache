package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"path/filepath"
	"strings"

	"github.com/extrame/xls"
	xls2 "github.com/shakinm/xlsReader/xls"
	"github.com/xuri/excelize/v2"
)

func ExcelizeTest() {
	// 1. 打开要转换的 XLS 文件
	file, err := excelize.OpenFile("/home/zoe/Downloads/test.xls")
	if err != nil {
		log.Fatalf("无法打开文件: %v", err)
	}

	// 2. 将文件保存为 XLSX 格式
	if err := file.SaveAs("output.xlsx"); err != nil {
		log.Fatalf("保存文件失败: %v", err)
	}

	fmt.Println("转换成功！文件已保存为 output.xlsx")
}

// XlsToXlsx converts an XLS stream to an XLSX stream
// by first reading the entire input into memory.
func XlsToXlsx(xlsReader io.Reader) (io.Reader, error) {
	// 1. Read the entire XLS file stream into a buffer.
	//    This is necessary to create a Seekable stream.
	xlsData, err := io.ReadAll(xlsReader)
	if err != nil {
		return nil, fmt.Errorf("failed to read XLS stream into memory: %w", err)
	}

	// 2. Wrap the buffer with bytes.NewReader, which implements io.ReadSeeker.
	seekableReader := bytes.NewReader(xlsData)

	// 3. Now, pass the seekable reader to the library.
	xlsFile, err := xls.OpenReader(seekableReader, "utf-8")
	if err != nil {
		return nil, fmt.Errorf("failed to open XLS file from stream: %w", err)
	}

	// 4. Continue with the conversion logic as before.
	sheet := xlsFile.GetSheet(0)
	if sheet == nil {
		return nil, fmt.Errorf("XLS file has no sheets")
	}

	xlsxFile := excelize.NewFile()
	sheetName := "Sheet1"

	for i := 0; i < int(1); i++ {
		row := sheet.Row(i)
		if row == nil || row.LastCol() == 0 {
			continue
		}

		for j := 0; j < row.LastCol(); j++ {
			cellValue := row.Col(j)
			cellName, err := excelize.CoordinatesToCellName(j+1, i+1)
			if err != nil {
				return nil, fmt.Errorf("failed to get cell name: %w", err)
			}
			if err := xlsxFile.SetCellValue(sheetName, cellName, cellValue); err != nil {
				return nil, fmt.Errorf("failed to write cell value: %w", err)
			}
		}
	}

	// 5. Write the new XLSX file to a buffer and return its reader.
	var b bytes.Buffer
	if _, err := xlsxFile.WriteTo(&b); err != nil {
		return nil, fmt.Errorf("failed to write XLSX to buffer: %w", err)
	}

	return &b, nil
}

// ConvertXLSToXLSX now returns the concrete *excelize.File type.
func ConvertXLSToXLSX(source io.Reader, charset string) (*excelize.File, error) {
	buf, err := io.ReadAll(source)
	if err != nil {
		return nil, fmt.Errorf("failed to read source stream into buffer: %w", err)
	}

	reader := bytes.NewReader(buf)
	workbook, err := xls.OpenReader(reader, charset)
	if err != nil {
		return nil, fmt.Errorf("opening XLS stream failed: %w", err)
	}

	xlsxFile := excelize.NewFile()
	xlsxFile.DeleteSheet("Sheet1")

	for i := 0; i < workbook.NumSheets(); i++ {
		sheet := workbook.GetSheet(i)
		if sheet == nil {
			continue
		}

		sheetName := sheet.Name
		_, err := xlsxFile.NewSheet(sheetName)
		if err != nil {
			return nil, fmt.Errorf("creating sheet '%s' failed: %w", sheetName, err)
		}

		for rowIndex := 0; rowIndex <= int(sheet.MaxRow); rowIndex++ {
			row := sheet.Row(rowIndex)
			if row == nil {
				continue
			}

			for colIndex := 0; colIndex < row.LastCol(); colIndex++ {
				cellValue := row.Col(colIndex)
				cellName, _ := excelize.CoordinatesToCellName(colIndex+1, rowIndex+1)
				xlsxFile.SetCellValue(sheetName, cellName, cellValue)
			}
		}
	}

	return xlsxFile, nil
}

func xls2xlsx(xlsFile string) {
	wb1, _ := xls2.OpenFile(xlsFile)
	newName := strings.TrimSuffix(xlsFile, filepath.Ext(xlsFile)) + ".xlsx"

	f2 := excelize.NewFile()
	for i := 0; i < wb1.GetNumberSheets(); i++ {
		ws1, _ := wb1.GetSheet(i)
		f2.NewSheet(ws1.GetName())
		maxrows := ws1.GetNumberRows()
		for r := 0; r < maxrows; r++ {
			r1, _ := ws1.GetRow(r)
			cols := r1.GetCols()
			for c, cs := range cols {
				ax, _ := excelize.CoordinatesToCellName(c+1, r+1)
				f2.SetCellValue(ws1.GetName(), ax, cs.GetString())
			}
		}
	}
	if len(f2.GetSheetList()) > wb1.GetNumberSheets() {
		f2.DeleteSheet("Sheet1") //NewFile默认新建的Sheet1(必须填写新Sheet后才生效)
	}
	fmt.Printf("> %q 转换完成，正在保存...\n", newName)
	f2.SaveAs(newName)
	f2.Close()
}

func ReadXls(filePath string) (res [][]string) {
	if xlFile, err := xls.Open(filePath, "utf-8"); err == nil {
		fmt.Println(xlFile.Author)
		//第一个sheet
		sheet := xlFile.GetSheet(0)
		temp := make([][]string, sheet.MaxRow)
		for i := 0; i < 1; i++ {
			row := sheet.Row(i)
			data := make([]string, 0)
			if row.LastCol() > 0 {
				for j := 0; j < row.LastCol(); j++ {
					col := row.Col(j)
					data = append(data, col)
				}
				temp[i] = data
			}
		}
		res = append(res, temp...)

	} else {
		log.Fatalf(fmt.Sprintf("failed to open xls file: %v", err))
	}
	return res
}

func main() {
	xls2xlsx("/home/zoe/Downloads/test.xls")
}
