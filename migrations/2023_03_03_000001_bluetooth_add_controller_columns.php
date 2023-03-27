<?php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Capsule\Manager as Capsule;

class BluetoothAddControllerColumns extends Migration
{
    private $tableName = 'bluetooth';

    public function up()
    {
        $capsule = new Capsule();
        $capsule::schema()->table($this->tableName, function (Blueprint $table) {
            $table->string('controller_chipset')->nullable();
            $table->string('controller_firmware')->nullable();
            $table->string('device_firmware')->nullable();
            $table->string('device_productid')->nullable();
            $table->string('device_vendorid')->nullable();
        });
    }
    
    public function down()
    {
        $capsule = new Capsule();
        $capsule::schema()->table($this->tableName, function (Blueprint $table) {
            $table->dropColumn('controller_chipset');
            $table->dropColumn('controller_firmware');
            $table->dropColumn('device_firmware');
            $table->dropColumn('device_productid');
            $table->dropColumn('device_vendorid');
        });
    }
}
