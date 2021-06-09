# -*- coding: utf-8 -*-

import openpyxl
from openpyxl.styles import Side, Border, colors
import pdb

class XLSBorder(object):
    def __init__(self):

        pass

    #定义边框样式
    def my_border(self, t_border, b_border, l_border, r_border):
        border = Border(top=Side(border_style=t_border, color=colors.BLACK),
                        bottom=Side(border_style=b_border, color=colors.BLACK),
                        left=Side(border_style=l_border, color=colors.BLACK),
                        right=Side(border_style=r_border, color=colors.BLACK))
        return border

    #初始化制定区域边框为所有框线
    def format_border(self, area, sheet):
        left = area.split(':')[0]
        right = area.split(':')[1]
        s_column = left[0]
        s_index = int(left[1:])
        e_column = right[0]
        e_index = int(right[1:])
        for row in tuple(sheet[s_column + str(s_index):e_column + str(e_index)]):
            for cell in row:
                cell.border = self.my_border('thin', 'thin', 'thin', 'thin')

    #给指定区域设置粗匣框线
    def set_solid_border(self, area, sheet):
        # for area in area_list:
        left = area.split(':')[0]
        right = area.split(':')[1]
        s_column = left[0]
        s_index = int(left[1:])
        e_column = right[0]
        e_index = int(right[1:])
        # pdb.set_trace()
        # s_column = area[0]
        # s_index = area[1]
        # e_column = area[2]
        # e_index = area[3]
        #设置左粗框线
        for cell in sheet[s_column][s_index - 1:e_index]:
            cell.border = self.my_border(cell.border.top.style, cell.border.bottom.style,
                                    'medium', cell.border.right.style)
        # 设置右粗框线
        for cell in sheet[e_column][s_index - 1:e_index]:
            cell.border = self.my_border(cell.border.top.style, cell.border.bottom.style,
                                    cell.border.left.style, 'medium')
        # 设置上粗框线
        for row in tuple(sheet[s_column + str(s_index):e_column + str(s_index)]):
            for cell in row:
                cell.border = self.my_border('medium', cell.border.bottom.style,
                                        cell.border.left.style, cell.border.right.style)
        # 设置下粗框线
        for row in tuple(sheet[s_column + str(e_index):e_column + str(e_index)]):
            for cell in row:
                cell.border = self.my_border(cell.border.top.style, 'medium',
                                        cell.border.left.style, cell.border.right.style)


# if __name__ == '__main__':
#     # wb = openpyxl.load_workbook('test.xlsx')
#     wb = openpyxl.Workbook()
#     sheet = wb['Sheet']
#     xlsBorder = XLSBorder()
#     xlsBorder.format_border('A3:D10', sheet)
#     for area in ['A3:D5', 'A6:D7', 'A8:D10', 'A3:A10', 'B3:C10', 'D3:D10']:
#
#         xlsBorder.set_solid_border(area, sheet)
#     wb.save('test.xlsx')