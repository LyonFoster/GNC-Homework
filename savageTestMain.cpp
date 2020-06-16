//savageTestMain.cpp

#include "savageFunctions.h"
#include <iostream>
#include <cmath>
#include <cstdlib>
#include <string>
#include <Eigen/Dense>


int main()
{

	// Eigen::Matrix2d m;
	// 	m(0,0) = 1;
	// 	m(0,1) = 2;
	// 	m(1,0) = 3;
	// 	m(1,1) = 4;

	// std::cout << m << std::endl;

	// Eigen::Vector3d testVec;
	// 	testVec << 1,2,3;
	// 	// testVec(1) = 2;
	// 	// testVec(2) = 3;

	// std::cout << testVec << std::endl;


	// //instance of the class
	savageFunctions savageObject;
	// std::cout << savageObject.skew(testVec) << std::endl;

	Eigen::Matrix3d dcm;
	dcm << 1, 0, 0, 0, 1, 0, 0, 0, 1;

	Eigen::Vector3d acc;
	acc << 1.31, -2.5, 4.37;

	Eigen::Vector3d omega;
	omega << 0.23,0.42,-0.11;

	double t = .54;

	Eigen::VectorXd state(9);
	state << 0,0,0,0,0,0,0,0,0;

	std::cout << savageObject.stateIntegrate(omega, acc, state, dcm, t) << std::endl;








	
	return 0;
}