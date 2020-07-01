#include <iostream>
#include <assert.h>
#include <set>
#include <vector>
#include <string>
#include "sudoku.h"

void line_printer() {
	for (int k = 0; k < 19; ++k) std::cout << '-';
	std::cout << std::endl;
}
// print() prints the sudoku table in a fancy way.
// effects: produces output.
void Table::print() {
	for (int j = 0; j < 9; ++j) {
		// get and transform data.
		std::string row_string[9];
		for (int k = 0; k < 9; ++k) {
			if (rows[j][k] == 0) { row_string[k] = ' '; }
			else { row_string[k] = '0' + rows[j][k]; }
		}
		// print the horizontal border
		if (j % 3 == 0) line_printer();
		// print row j.
		for (int k = 0; k < 9; ++k) {
			if (k % 3 == 0) { std::cout << '|' << row_string[k]; }
			else { std::cout << ' ' << row_string[k]; }
		}
		std::cout << '|' << std::endl;
	}
	line_printer();
}

// row_check(row) performs row check on the specified row. return 1 if there is no duplicates and 0 otherwise.
// requires: row >= 0
//           row <= 8
// effects: none
int Table::row_check(int row) {
	assert(row >= 0);
	assert(row <= 8);
	// get and transform data
	std::set<int> data;
	int count = 0;
	for (int j = 0; j < 9; ++j) {
		if (rows[row][j] != 0) {
			++count;
			data.insert(rows[row][j]);
		}
	}
	return count == data.size();
}

// col_check(col) performs column check on the specified column. return 1 if there is no duplicates and 0 otherwise.
// requires: col >= 0
//           col <= 8
// effects: none
int Table::col_check(int col) {
	assert(col >= 0);
	assert(col <= 8);
	// get and transform data
	std::set<int> data;
	int count = 0;
	for (int j = 0; j < 9; ++j) {
		if (cols[col][j] != 0) {
			++count;
			data.insert(cols[col][j]);
		}
	}
	return count == data.size();
}

// blo_check(blo) performs block check on the specified block. return 1 if there is no duplicates and 0 otherwise.
// requires: blo >= 0
//           blo <= 8
// effects: none
int Table::blo_check(int blo) {
	assert(blo >= 0);
	assert(blo <= 8);
	// get and transform data
	std::set<int> data;
	int count = 0;
	for (int j = 0; j < 9; ++j) {
		if (blos[blo][j] != 0) {
			++count;
			data.insert(blos[blo][j]);
		}
	}
	return count == data.size();
}

int Table::is_valid(int row, int col) {
	assert(row >= 0);
	assert(row <= 8);
	assert(col >= 0);
	assert(col <= 8);
	int blo = (row / 3) * 3 + col / 3;
	assert(blo >= 0);
	assert(blo <= 8);
	return row_check(row) &&
		col_check(col) &&
		blo_check(blo);
}

// helper for is_valid, checks if the each cell in the table is filled with some number.
int Table::is_full() {
	for (int row = 0; row < 9; ++row) {
		for (int col = 0; col < 9; ++col) {
			if (rows[row][col] == 0) { return 0; }
		}
	}
	for (int col = 0; col < 9; ++col) {
		for (int row = 0; row < 9; ++row) {
			assert(cols[col][row]);
		}
	}
	for (int blo = 0; blo < 9; ++blo) {
		for (int blo_index = 0; blo_index < 9; ++blo_index) {
			assert(blos[blo][blo_index]);
		}
	}
	return 1;
}

// checks correctness of solution.
int Table::is_solved() {
	if (!is_full()) { return 0; }
	for (int j = 0; j < 9; ++j) {
		if (!row_check(j)) { return 0; }
		if (!col_check(j)) { return 0; }
		if (!blo_check(j)) { return 0; }
	}
	return 1;
}

// return_empty_cells() returns a set of integer indices at which the cell is empty.
std::vector<int> Table::return_empty_cells() {
	// get data using a vector
	std::vector<int> empty_cells;
	for (int row = 0; row < 9; ++row) {
		for (int col = 0; col < 9; ++col) {
			if (rows[row][col] == 0) {
				int index = row * 9 + col;
				empty_cells.push_back(index);
			}
		}
	}
	return empty_cells;
}

// start checking form the next number in the specified cell till 9.
// fills the cell with the next valid number and return 1 indicating success and
// sets back the cell to empty and return 0 indicating failure.
int Table::fill_cell(int row, int col) {
	assert(row >= 0);
	assert(row <= 8);
	assert(col >= 0);
	assert(col <= 8);
	int blo = (row / 3) * 3 + col / 3;
	int blo_index = (row - (row / 3) * 3) * 3 + (col - (col / 3) * 3);
	assert(blo >= 0);
	assert(blo <= 8);
	assert(blo_index >= 0);
	assert(blo_index <= 8);

	int current_num = rows[row][col];
	assert(cols[col][row] == current_num);
	assert(blos[blo][blo_index] == current_num);

	// try each number until we find a valid one.
	int start_num = current_num + 1;
	for (int n = start_num; n <= 9; ++n) {
		rows[row][col] = n;
		cols[col][row] = n;
		blos[blo][blo_index] = n;
		if (is_valid(row, col)) { return 1; }
	}
	// if we reach here, that means no number can fill into this cell.
	rows[row][col] = 0;
	cols[col][row] = 0;
	blos[blo][blo_index] = 0;
	return 0;
}

int Table::back(std::vector<int> empty_cells, int current_index) {
	int index = current_index - 1;
	while (1) {
		if (index >= 0) {
			int cell_index = empty_cells[index];
			int row = cell_index / 9;
			int col = cell_index % 9;
			int success = fill_cell(row, col);
			if (success) { return index; }
			else { --index; }
		}
		else {
			return -1;
		}
	}
}

int Table::solve() {
	std::vector<int> blanks = return_empty_cells();
	int length = blanks.size();
	int index = 0;
	while (1) {
		// check the cell indicated by the cell_index located at index in the blanks.
		int cell_index = blanks[index];
		int row = cell_index / 9;
		int col = cell_index % 9;
		int success = fill_cell(row, col);
		if (success) { ++index; }
		else { index = back(blanks, index) + 1; }
		if (index < 0) {
			std::cout << "cannot solve???";
			return 0;
		}
		else if (index >= length) {
			std::cout << "successfully solved:" << std::endl;
			return 1;
		}
	}
}

int main() {
	Table table;
	for (int j = 0; j < 9; ++j) {
		std::string input;
		std::cin >> input;
		for (int k = 0; k < 9; ++k) {
			table.rows[j][k] = input[k] - '0';
		}
	}
	for (int col = 0; col < 9; ++col) {
		for (int row = 0; row < 9; ++row) {
			table.cols[col][row] = table.rows[row][col];
		}
	}
	for (int blo = 0; blo < 9; ++blo) {
		for (int blo_index = 0; blo_index < 9; ++blo_index) {
			int row = (blo / 3) * 3 + (blo_index / 3);
			int col = (blo % 3) * 3 + (blo_index % 3);
			assert(table.rows[row][col] == table.cols[col][row]);
			table.blos[blo][blo_index] = table.rows[row][col];
		}
	}
	table.print();
	table.solve();
	table.print();
}