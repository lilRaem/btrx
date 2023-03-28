from btrx import Btrx
import main_search

def main():
	btrx_list = Btrx.get_product_list()
	print(btrx_list)
	main_search.search()

if __name__ == "__main__":
	main()