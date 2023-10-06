using System;
using System.Collections.Generic;

class Program
{



    // Check if the number is odd
    bool IsEven(int n)
    {
        return n % 2 == 0;
    }

    /*
    * If there are duplicates within the list passed as a parameter, this function
    * removes them, so that there are no duplicated elements.
    * 
    * Args: items (List<T>): The list from which duplicates will be removed.
    * 
    * Returns: List<T>: A new list with duplicates removed.
    */
    List<T> RemoveDuplicates<T>(List<T> items)
    {
        List<T> uniqueItems = new List<T>();

        foreach (T item in items)
        {
            if (!uniqueItems.Contains(item))
            {
                uniqueItems.Add(item);
            }
        }

        return uniqueItems;
    }


}