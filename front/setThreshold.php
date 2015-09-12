<!DOCTYPE html>
<html>
<head>
    <title>Set Threshhold</title>
    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
    <link href="set.css" rel="stylesheet" media="screen">
    <script src="jquery.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script type="text/javascript" src="right.js"></script>
    <script src="right-slider.js"></script>
</head>
<body>
<?php
  $a="/home/xiejl/OSS/PAQM/bin/setThresholdMoz.sh";
  if(isset($_POST["minThre"]) & isset($_POST["maxThre"])){
    $a=$a." ".($_POST["minThre"]/100.0)." ".($_POST["maxThre"]/100.0);
  }
  #echo $a."<br/>";
  $res=exec($a);
  #echo $res;
  $arr=split(",",$res);
  //ouput content
  #echo "<p> Red Flag: color bottom ".($arr[0]*100)."% with value ".$arr[2]."</p>";
  #echo "<p> Green Flag: color top ".((1 - $arr[1])*100)."% with value ".$arr[3]."</p>";
?>
<header class="navbar navbar-default navbar-fixed-top bs-docs-nav" role="banner">
  <div class="container">
    <div class="navbar-header">
      <button class="navbar-toggle" type="button" data-toggle="collapse" data-target=".bs-navbar-collapse">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <div class="navbar-brand">Data Source: Mozilla Bugzilla</div>
    </div>
    <nav class="collapse navbar-collapse bs-navbar-collapse" role="navigation">
      <ul class="nav navbar-nav navbar-right">
        <li>
          <div class="navbar-brand">Time Span: 2001-2011</div>
        </li>
      </ul>
    </nav>
  </div>
</header>

     

    <div id="main">
        <div id="header">
            <p>Set Threshhold</p>
        </div>
        <form id="form1" name="form1" method="post" action="/projects/paar/setThreshold.php">
            <h3>Warn</h3>
            <div class="rui-slider" <?php echo "data-slider=\"{min:0,max:100,value:".($arr[0]*100).",update:'left'}\" "?> >
                <div class="level"></div>
                <div class="handle"></div>
            </div>
            <input class="percent" type="text" id="left" name="minThre" />%

            <h3>Recommend</h3>
            <div class="rui-slider" <?php echo "data-slider=\"{min:0,max:100,value:".($arr[2]*100).",update:'right'}\" "?> >
                <div class="level"></div>
                <div class="handle"></div>
            </div>
            <input class="percent" type="text" id="right" name="maxThre" />%

            <br/>
            <br/>

            <input type="submit" value="Submit" class="btn btn-primary" />
           
        </form>
        <br>
         <a  href="/projects/paar/index.html"><button class="btn btn-primary">Back </button></a>

        

        <h2 style="margin-top:30px">Now:</h2>
        <p class="report"> Recommending Threshold: Recommend the issue when the probability of being correct of its assignment is greater than <b><?php echo number_format($arr[3], 2, '.', '') ?></b> (<b><?php echo $arr[2]*100 ?> </b>% quantile)</p>
        <p class="report"> Warning Threshold: Give warning when the probability of being correct of the assignment is less than <b><?php echo number_format($arr[1], 2, '.', '') ?></b> (<b><?php echo $arr[0]*100 ?></b>% quantile)</p>


    </div>
    
</body>
</html>
