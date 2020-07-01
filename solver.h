#include <vector>

class Table {
public:
	int rows[9][9];
	int cols[9][9];
	int blos[9][9];
	int row_check(int row);
	int col_check(int col);
	int blo_check(int blo);
	int is_valid(int row, int col);
	int is_full();
	int is_solved();
	std::vector<int> return_empty_cells();
	int fill_cell(int row, int col);
	int back(std::vector<int> empty_cells, int current_index);
	void print();
	int solve();
};