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
#include "Randomaxis.h"
#include "random.h"
#include "pi.h"

static const std::string _module_id("$Id$");

QString Randomaxis::ModelID(void) {
  // specify the name of your model here
  return QString( "Thesis Willem: Random axis division" );
}

// return the number of chemicals your model 
int Randomaxis::NChem(void) { return 1; }

// To be executed after cell divisi
void Randomaxis::OnDivide(ParentInfo *parent_info, CellBase *daughter1, CellBase *daughter2) {
  // rules to be executed after cell division go here
  // (e.g., cell differentiation rules)
}

void Randomaxis::SetCellColor(CellBase *c, QColor *color) { 
  // add cell coloring rules here

  double blueTint = (c->Chemical(0) - 0) * (255 - 0) / (2000 - 255) + 0;
  
  color -> setRgb(0,0, blueTint);

}

void Randomaxis::CellHouseKeeping(CellBase *c) {
  // add cell behavioral rules here

  if (c->Chemical(0) < 100) {
    c->SetTargetArea(100);
    c->SetChemical(0, 100);
  } else {
    c->SetTargetArea(c->Chemical(0));
  }

	if (c->Area() > par->rel_cell_div_threshold * c->BaseArea()) {
    
		double plane = Pi*RANDOM();
    Vector axis(sin(plane), cos(plane), 0.0);

    c->DivideOverAxis(axis);
	}//if


}

void Randomaxis::CelltoCellTransport(Wall *w, double *dchem_c1, double *dchem_c2) {
  // add biochemical transport rules her

  if (w->C1()->BoundaryPolP() || w->C2()->BoundaryPolP()) {
    return;
  } //if

  //symplastic flux, see equation 8
  // U_ij = A * L *(P_i-P_j)
  double turgorcelli = 2*(w->C1()->Chemical(0) - w->C1()->Area());
  double turgorcellj = 2*(w->C2()->Chemical(0) - w->C2()->Area());
  //double turgorcelli = w->C1()->Chemical(0); // P_i
  //double turgorcellj = w->C2()->Chemical(0); // P_j

  //double turgorcelli = 2*(w->C1()->TargetArea() - w->C1()->chem[0]);

  double symplasticFlux = w->Length() * par->kt * (turgorcellj - turgorcelli); //A_i * L^s * (P_j - P_i) Basically Ficks law

  //phi_s_real = (2* w->Length() * par->i1)/w->Length();
  
  dchem_c1[0] += symplasticFlux;
  dchem_c2[0] -= symplasticFlux;
  

}
void Randomaxis::WallDynamics(Wall *w, double *dw1, double *dw2) {
  // add biochemical networks for reactions occuring at walls here
}
void Randomaxis::CellDynamics(CellBase *c, double *dchem) { 
  // add biochemical networks for intracellular reactions here

  double walllength = c->ExactCircumference(); //A_i
  double turgor = 2*(c->Chemical(0) - c->Area()); // P_i
  //double turgor = c->Chemical(0);

  
  // Assymplastic Flux, see equation 8 in the paper
  double flux = walllength * par->kc * ((100 - turgor)*1e-5); // A_i * L^a * (P^M - P_i)

  //double phi_a_real = (walllength * permeability_a)/walllength;

  dchem[0] += flux;

}


//Q_EXPORT_PLUGIN2(Randomaxis, Randomaxis)
