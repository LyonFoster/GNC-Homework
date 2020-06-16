	#include "savageFunctions.h"
#include <iostream>
#include <cmath>
#include <cstdlib>
#include <string>
#include <Eigen/Dense>

// a little documentation up front:
// an eigen vector is what you'd expect--a vector that only scales in a linear transformation
// an "Eigen" vector is a vector using the Eigen api

// also, it's pretty convenient that eigen objects work as regular objects for pass by value and return by value
// so that's nice to keep in mind



Eigen::Matrix3d savageFunctions::skew(Eigen::Vector3d v)
{//pass in an "Eigen" vector

	//initialize a "skewwed" matrix
	Eigen::Matrix3d skewwed;

	//populate the "skewwed" matrix
	skewwed <<    0, -v(2),  v(1), 
			   v(2),     0, -v(0),
			  -v(1),  v(0),     0;

  //return the skewwed matrix
  return skewwed;
}

Eigen::VectorXd savageFunctions::stateIntegrate(Eigen::Vector3d omega, Eigen::Vector3d accel,
												  Eigen::VectorXd prevState, Eigen::Matrix3d prevDCM, double d_t)
{
	//state of form,
	// 0 x 
	// 1 y
	// 2 z
	// 3 v_x
	// 4 v_y
	// 5 v_z
	// 6 a_x
	// 7 a_y
	// 8 a_z

	//and of course the previous dcm is needed

	//EVERY PARAMETER must be of the "Eigen" type

	//Okay getting started here
	//First things first,
	//use the previous time step DCM and the current angular rates to 
	//find the current derivative of the current DCM
	//the d_ will be used to denore a time rate of change for something that doesn't have a 
	//standard usage (eg. theta->omega)
	//taken from 3-53 of savage (eq. 3.3.2-6)
	Eigen::Matrix3d d_DCM = prevDCM * skew(omega);

	//calculate the current DCM
	Eigen::Matrix3d DCM = d_DCM * d_t + prevDCM;

	// use the current DCM to convert acceleration to the inertial frame
	Eigen::Vector3d accelInertial = DCM * accel;

	//okay now working down through the state vector and integrating as I go

							
	Eigen::VectorXd state(9);  // x               v*t                 .5at^2
	               state << prevState[0] + prevState[3] * d_t + accelInertial[0] * pow(d_t,2) * .5, //x
							prevState[1] + prevState[4] * d_t + accelInertial[1] * pow(d_t,2) * .5, //y
							prevState[2] + prevState[5] * d_t + accelInertial[2] * pow(d_t,2) * .5, //z
							 // v                 a*t
							prevState[3] + accelInertial[0] * d_t, //v_x
							prevState[4] + accelInertial[1] * d_t, //v_y
							prevState[5] + accelInertial[2] * d_t, //v_z
							 // a
							accelInertial[0], //a_x
							accelInertial[1], //a_y
							accelInertial[2]; //a_z

	std::cout << DCM << std::endl;

	return state;
} s


