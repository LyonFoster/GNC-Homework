
#ifndef SAVAGE_FUNCTIONS_26MAY2020
#define SAVAGE_FUNCTIONS_26MAY2020

#include "savageFunctions.h"
#include <iostream>
#include <cmath>
#include <cstdlib>
#include <string>
#include <Eigen/Dense>


class savageFunctions
{

public:
	savageFunctions(){}
	

	Eigen::Matrix3d skew(Eigen::Vector3d v);

	Eigen::VectorXd stateIntegrate(Eigen::Vector3d omega, Eigen::Vector3d accel,
								   Eigen::VectorXd prevState, Eigen::Matrix3d prevDCM, double d_t);

};






	

#endif //SAVAGE_FUNCTIONS_26MAY2020