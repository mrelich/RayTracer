
#include "../Simulation/scripts/myHist.C"

test()
{

  // Make canvas
  TCanvas* c = makeCanvas("c");
  
  // Make generic hist
  TH1F* hist = makeHist("hist",1,-1,1,"","",kBlack,20);
  hist->SetMinimum(-0.7);
  hist->SetMaximum(0.7);
  hist->Draw();

  // Axis
  TLine* yaxis = makeLine(0,0,-0.5,0.5,kBlack,1); yaxis->Draw("same");

  // Make lines for normal block
  TLine* top   = makeLine(-0.5,0.5,0.15,0.15,kBlue,1);   top->Draw("same");
  TLine* bot   = makeLine(-0.5,0.5,-0.15,-0.15,kBlue,1); bot->Draw("same");
  TLine* right = makeLine(0.5,0.5,-0.15,0.15,kBlue,1);   right->Draw("same");
  TLine* left  = makeLine(-0.5,-0.5,-0.15,0.15,kBlue,1); left->Draw("same");
  
  // Now experiment to try to get this right...
  double angle = -30 * TMath::Pi()/180.;
  //double angle = 0;
  cout<<"tan(angle): "<<tan(angle)<<" "<<-1/tan(angle)<<endl;

  // top
  double x0 = -0.5, x1 = 0.5, y0 = 0.15, y1 = 0.15;
  rotation(angle,x0,y0); rotation(angle,x1,y1);
  double slope = (y1-y0)/(x1-x0);
  printEq(slope,x0,y0);
  TLine* ntop = makeLine(x0,x1,y0,y1,kRed,1); ntop->Draw("same");
  
  
  // bot
  x0 = -0.5; x1 = 0.5; y0 = -0.15; y1 = -0.15;
  rotation(angle,x0,y0); rotation(angle,x1,y1);
  slope = (y1-y0)/(x1-x0);
  printEq(slope,x0,y0);
  //cout<<"Bottom slope: "<<(y1-y0)/(x1-x0)<<endl;
  TLine* nbot = makeLine(x0,x1,y0,y1,kRed,1); nbot->Draw("same");

  // right
  x0 = 0.5; x1 = 0.5, y0 = -0.15; y1 = 0.15;
  rotation(angle,x0,y0); rotation(angle,x1,y1);
  slope = (y1-y0)/(x1-x0);
  printEq(slope,x0,y0);
  //cout<<"Right slope: "<<(y1-y0)/(x1-x0)<<endl;
  TLine* nR = makeLine(x0,x1,y0,y1,kRed,1); nR->Draw("same");
  
  // left
  x0 = -0.5; x1 = -0.5; y0 = -0.15; y1 = 0.15;
  rotation(angle,x0,y0); rotation(angle,x1,y1);
  slope = (y1-y0)/(x1-x0);
  printEq(slope,x0,y0);
  TLine* nL = makeLine(x0,x1,y0,y1,kRed,1); nL->Draw("same");

  // Testing
  TF1* ftop = new TF1("top","-0.57735026919*(x-0.3) + 0.173205080757",-1,1);
  ftop->Draw("same");
    
}

void printEq(double slope, double x, double y)
{
  cout<<"Eq: "<<slope<<"*(x-"<<x<<") + "<<y<<endl;
}

double rotation(double angle, double &x, double &y)
{
  
  double prevX = x;
  double prevY = y;

  x = cos(angle)*prevX - sin(angle)*prevY;
  y = sin(angle)*prevX + cos(angle)*prevY;
  

}
