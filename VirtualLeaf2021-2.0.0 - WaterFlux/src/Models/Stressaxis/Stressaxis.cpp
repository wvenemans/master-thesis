/*
 *
 *  This file is part of the Virtual Leaf.
 *
 *  The Virtual Leaf is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  The Virtual Leaf is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with the Virtual Leaf.  If not, see <http://www.gnu.org/licenses/>.
 *
 *  Copyright 2010 Roeland Merks.
 *
 */

#include <QObject>
#include <QtGui>

#include "parameter.h"

#include "wallbase.h"
#include "cellbase.h"
#include "Stressaxis.h"

static const std::string _module_id("$Id$");

QString Stressaxis::ModelID(void) {
  // specify the name of your model here
  return QString( "Thesis Willem: Stress based division" );
}

// return the number of chemicals your model 
int Stressaxis::NChem(void) { return 1; }

// To be executed after cell divisi
void Stressaxis::OnDivide(ParentInfo *parent_info, CellBase *daughter1, CellBase *daughter2) {
  // rules to be executed after cell division go here
  // (e.g., cell differentiation rules)
}

void Stressaxis::SetCellColor(CellBase *c, QColor *color) { 
  // add cell coloring rules here

}

void Stressaxis::CellHouseKeeping(CellBase *c) {
  // add cell behavioral rules here


  c->EnlargeTargetArea(par->cell_expansion_rate);
	if (c->Area() > par->rel_cell_div_threshold * c->BaseArea()) {
    /*
		double stress;
    Vector stress_axis;
    double xaxis;
    double yaxis;
    c->Stress(&stress, &stress_axis, &xaxis, &yaxis);
    std::cout << "Stress: " << stress << std::endl;
    std::cout << "Stress axis: " << stress_axis.x << " " << stress_axis.y << " " << stress_axis.z << std::endl;
    std::cout << "X axis: " << xaxis << std::endl;
    std::cout << "Y axis: " << yaxis << std::endl;
    c->DivideOverAxis(stress_axis);
    */
	}//if


}

void Stressaxis::CelltoCellTransport(Wall *w, double *dchem_c1, double *dchem_c2) {
  // add biochemical transport rules her
  

}
void Stressaxis::WallDynamics(Wall *w, double *dw1, double *dw2) {
  // add biochemical networks for reactions occuring at walls here
}
void Stressaxis::CellDynamics(CellBase *c, double *dchem) { 
  // add biochemical networks for intracellular reactions here

}


//Q_EXPORT_PLUGIN2(Stressaxis, Stressaxis)
