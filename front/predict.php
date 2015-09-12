<!DOCTYPE html>
<html>
<head>
    <title>PAAR</title>
    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">
    <link rel="stylesheet" type="text/css" href="result.css">
</head>
<body>

<?php
$bugid = $_GET["bugid"];
$cmd = "/home/xiejl/OSS/PAQM/bin/runPredictMoz.sh ".$_GET["bugid"];
$result = exec($cmd);
$arr = split(",", $result);
$error = true;
if ($arr[0] == "Error") {
    $error = true;
} else {
    $error = false;
    $login=$arr[0];
    $date=$arr[1];
    $new=$arr[2];
    $predict=$arr[11];
    $maxThre=$arr[13];
    $minThre=$arr[12];
    $nPrdCorAssi=$arr[3];
    $nPrdAssi=$arr[4];
    $prdCorRat=$nPrdCorAssi/$nPrdAssi;
    $nLogPrdCorAssi=$arr[5];
    $nLogPrdAssi=$arr[6];
    $prdLogCorRat=$nLogPrdCorAssi/$nLogPrdAssi;
    $cntMaxExp=$arr[7];
    $cntN=$arr[8];
    $cmtN=$arr[9];
    $role=$arr[10];

}
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

<?php
    if ($error) {
        echo "<div id=\"main\">";
        if($arr[1] == "noSuchBug"){
            echo "<div id=\"error\">"."Can not find bug ".$_GET["bugid"]."</div>";
        }
        else {
            echo "<div id=\"error\">"."No need to predict the correctness of the assignment"."</div>";
        }

        echo "</div>";
    } else {
?>
    <div id="main">
        <div id="top">
            <div id="buginfo">
                <h2>BugID: <?php echo $_GET["bugid"] ?></h2>
                <h3>Product: <?php echo $new?> </h3>
                <h3>Actor: <?php echo $login?></h3>
                <br>
                <br>
                <br>
            </div>
            <div id="prediction">
                <h2>Prediction:</h2>
<?php
if($predict > $maxThre){
    echo "<img src=\"recommend.png\" />";
}
else if($predict < $minThre){
    echo "<img src=\"warning.png\" />";
}
else{
    echo "<img src=\"notrecommend.png\" />";
}
?>
            </div>
        </div>

        <div id="metrics">
            <h2>Metrics Calculated</h2>
            <br/>
            <div id="product"></div>
            <h4>Product</h4>
            <table class="table table-hover">
                <tr>
                    <td>Product's Error Rate</td>
                    <td><?php echo number_format((1.0 - $prdCorRat), 2, '.', '') ?></td>
                </tr>
            </table>
            <div id="actor"></div>
            <h4>Actor</h4>
            <table class="table table-hover">
                <tr>
                    <td>Actor's Error Rate for The Product</td>
                    <td><?php echo number_format((1.0 - $prdLogCorRat), 2, '.', '') ?></td>
                </tr>
                <tr class>
                    <td >Maximum Experience over All Peers</td>
                    <td><?php echo $cntMaxExp?></td>
                </tr>
                <tr>
                    <td>Number of Actor's Peers</td>
                    <td><?php echo $cntN ?></td>
                </tr>
                <tr>
                    <td>Average Social Depth</td>
                    <td><?php echo number_format(($cmtN / (1 + $cntN)), 2, '.', '') ?></td>
                </tr>
                <tr>
                    <td>Actor's Role</td>
                    <td><?php echo $role ?></td>
                </tr>
            </table>

        </div>
    </div>
<?php } ?>

    <script src="jquery.js"></script>
    <script src="js/bootstrap.min.js"></script>
</body>
</html>
