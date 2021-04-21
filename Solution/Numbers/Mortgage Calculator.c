// Calculate the monthly payments of a fixed term mortgage over given Nth terms at a given interest rate.
//This program is the C equivalent of the Java Program by francis36012

#include <stdio.h>

double computeMonthlyPayment(double loan, float interestRate, int term);
float exponentialFunction(float base, int months);

void main(){
	
	double loan = 0;
	float interestRate = 0;
	float monthlyPayment = 0;
	float balance = 0;
	int compoundPeriod = 0;
	int term;
	
	printf("Enter loan amount: ");
	scanf("%lf", &loan);
	
	printf("Enter interest rate on loan: ");
	scanf("%f", &interestRate);
	
	printf("Enter term (in years) for the loan payment: ");
	scanf("%d", &term);
	
	printf("\n---------------------------------------------\n");
	
	monthlyPayment = computeMonthlyPayment(loan, interestRate, term);
	balance = (float) -(monthlyPayment * (term * 12));
	
	printf("Amount owed to bank : %.2f\n", balance);
	printf("Minimum monthly payment : %.2f\n", monthlyPayment);
	
	
}


// Computer monthly payment of a loan
double computeMonthlyPayment(double loan, float interestRate, int term){
	
	float rate = (interestRate / 100) / 12;
	float base = rate + 1;
	int months  = term * 12;
	float result = 0;
	result = (float) loan * (rate * exponentialFunction(base, months)) / (exponentialFunction(base, months) - 1);	// Calculation / Formula
	return result;
	
}

float exponentialFunction(float base, int months){		// power function
	int i; 	// counter variable
	float tempVar = 1;
	for(i = 0; i < months; i++){
		tempVar *= base;
	} 
	
	return tempVar;
	
}

