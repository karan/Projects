import java.util.Arrays;

public class MergeSort {

	public static void main(String[] args) {
		int[] nums = {9, 3, 15, 6, 2, 11, 5, 1, 10};
		mergeSort(nums);
		System.out.println(Arrays.toString(nums));
	}
	
	public static void mergeSort(int[] nums) {
		mergeSort(nums, 0, nums.length - 1);
	}
	
	private static void mergeSort(int[] nums, int start, int end) {
		if (start >= end) return;
		int med = start + ((end - start) / 2);
		mergeSort(nums, start, med);
		mergeSort(nums, med + 1, end);
		merge(nums, start, med, end);
	}
	
	private static void merge(int[] nums, int start, int med, int end) {
		int[] temp = new int[nums.length];
		for (int i = start; i <= end; i++) {
			temp[i] = nums[i];
		}
		
		int p1 = start;
		int p2 = med + 1;
		int tp = start;
		while (p1 <= med && p2 <= end) {
			if (nums[p1] < nums[p2]) {
				temp[tp] = nums[p1];
				p1++;
			} else {
				temp[tp] = nums[p2];
				p2++;
			}
			tp++;
		}
		if (p1 <= med) {
			for (int i = p1; i <= med; i++) {
				temp[tp] = nums[p1];
				tp++;
				p1++;
			}
		}
		for (int i = start; i <= end; i++) {
			nums[i] = temp[i];
		}
	}

}
