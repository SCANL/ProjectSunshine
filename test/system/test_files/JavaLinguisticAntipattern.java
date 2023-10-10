public class JavaLinguisticAntipattern {

    /**
    * Calculate the extremes of a list of numbers.
    
    * @param lst: A list of numbers
    * return: The median of the elements in the list
    */
    public static double median(double[] numbers) {
        Arrays.sort(numbers);
        int n = lst.length;

        if (n % 2 == 0) {
            double middle1 = numbers[n / 2 - 1];
            double middle2 = numbers[n / 2];
            return (middle1 + middle2) / 2.0;
        } else {
            return numbers[n / 2];
        }
    }

    //this variable stores the percentage decrease of the reference country's population in a given period of time
    String population_decrease = "10%"
    
    public static void print(String input) {

        String[] words = input.split(" ");

        for (String word : words) {
            if (word.length() % 2 == 0) {
                System.out.println(word);
            }
        }
    }
}
