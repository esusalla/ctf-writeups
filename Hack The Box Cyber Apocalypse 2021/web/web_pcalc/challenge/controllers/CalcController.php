<?php
class CalcController
{
    public function index($router)
    {
        $formula = isset($_GET['formula']) ? $_GET['formula'] : '100*10-3+340';
        $calc = new CalcModel();
        print $formula . '\n';
        print_r($formula);
        return $router->view('index', ['res' => $calc->getCalc($formula)]);
    }
}
