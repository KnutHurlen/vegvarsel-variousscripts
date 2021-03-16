CREATE PROCEDURE `create_model`(
	IN station_id varchar(45)
	)
BEGIN
	Create Temporary table vegvarsel.datelist
		select * from 
			(select adddate('2015-01-01',t4.i*10000 + t3.i*1000 + t2.i*100 + t1.i*10 + t0.i) thedate from
			 (select 0 i union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9) t0,
			 (select 0 i union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9) t1,
			 (select 0 i union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9) t2,
			 (select 0 i union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9) t3,
			 (select 0 i union select 1 union select 2 union select 3 union select 4 union select 5 union select 6 union select 7 union select 8 union select 9) t4) v
		where 
			(thedate between '2015-11-15' and '2016-05-20') OR
			(thedate between '2016-11-15' and '2017-05-20') OR
			(thedate between '2017-11-15' and '2018-05-20') OR
			(thedate between '2018-11-15' and '2019-05-20') OR
			(thedate between '2019-11-15' and '2020-05-20') 
		order by thedate asc
		limit 2000;

		Select 
			 theDate 
			, hist_pred_6h.station_id 
			, hist_pred_6h.air_temp as h6_air_temp
			, hist_pred_6h.precipitation_amount as h6_precipitation_amount
			, hist_pred_6h.wind_bearing as h6_wind_bearing
            , null as h6_wind_bearing_sin
            , null as h6_wind_bearing_cos
			, hist_pred_6h.wind_speed as h6_wind_speed
			, hist_pred_6h.cloud_area_fraction as h6_cloud_area_fraction
			, hist_pred_6h.air_pressure_at_sea_level as h6_air_pressure_at_sea_level
			, hist_pred_6h.relative_humidity as h6_relative_humidity
			, hist_pred_12h.air_temp as h12_air_temp
			, hist_pred_12h.precipitation_amount as h12_precipitation_amount
			, hist_pred_12h.wind_bearing as h12_wind_bearing
			, null as h12_wind_bearing_sin
            , null as h12_wind_bearing_cos
			, hist_pred_12h.wind_speed as h12_wind_speed
			, hist_pred_12h.cloud_area_fraction as h12_cloud_area_fraction
			, hist_pred_12h.air_pressure_at_sea_level as h12_air_pressure_at_sea_level
			, hist_pred_12h.relative_humidity as h12_relative_humidity
			, hist_pred_18h.air_temp as h18_air_temp
			, hist_pred_18h.precipitation_amount as h18_precipitation_amount
			, hist_pred_18h.wind_bearing as h18_wind_bearing
            , null as h18_wind_bearing_sin
            , null as h18_wind_bearing_cos
			, hist_pred_18h.wind_speed as h18_wind_speed
			, hist_pred_18h.cloud_area_fraction as h18_cloud_area_fraction
			, hist_pred_18h.air_pressure_at_sea_level as h18_air_pressure_at_sea_level
			, hist_pred_18h.relative_humidity as h18_relative_humidity
			, hist_pred_24h.air_temp as h24_air_temp
			, hist_pred_24h.precipitation_amount as h24_precipitation_amount
			, hist_pred_24h.wind_bearing as h24_wind_bearing
            , null as h24_wind_bearing_sin
            , null as h24_wind_bearing_cos
			, hist_pred_24h.wind_speed as h24_wind_speed
			, hist_pred_24h.cloud_area_fraction as h24_cloud_area_fraction
			, hist_pred_24h.air_pressure_at_sea_level as h24_air_pressure_at_sea_level
			, hist_pred_24h.relative_humidity as h24_relative_humidity
			, hist_pred_30h.air_temp as h30_air_temp
			, hist_pred_30h.precipitation_amount as h30_precipitation_amount
			, hist_pred_30h.wind_bearing as h30_wind_bearing
			, null as h30_wind_bearing_sin
            , null as h30_wind_bearing_cos
			, hist_pred_30h.wind_speed as h30_wind_speed
			, hist_pred_30h.cloud_area_fraction as h30_cloud_area_fraction
			, hist_pred_30h.air_pressure_at_sea_level as h30_air_pressure_at_sea_level
			, hist_pred_30h.relative_humidity as h30_relative_humidity
			, hist_pred_36h.air_temp as h36_air_temp
			, hist_pred_36h.precipitation_amount as h36_precipitation_amount
			, hist_pred_36h.wind_bearing as h36_wind_bearing
			, null as h36_wind_bearing_sin
            , null as h36_wind_bearing_cos
			, hist_pred_36h.wind_speed as h36_wind_speed
			, hist_pred_36h.cloud_area_fraction as h36_cloud_area_fraction
			, hist_pred_36h.air_pressure_at_sea_level as h36_air_pressure_at_sea_level
			, hist_pred_36h.relative_humidity as h36_relative_humidity
			, hist_pred_42h.air_temp as h42_air_temp
			, hist_pred_42h.precipitation_amount as h42_precipitation_amount
			, hist_pred_42h.wind_bearing as h42_wind_bearing
            , null as h42_wind_bearing_sin
            , null as h42_wind_bearing_cos
			, hist_pred_42h.wind_speed as h42_wind_speed
			, hist_pred_42h.cloud_area_fraction as h42_cloud_area_fraction
			, hist_pred_42h.air_pressure_at_sea_level as h42_air_pressure_at_sea_level
			, hist_pred_42h.relative_humidity as h42_relative_humidity
			, hist_pred_48h.air_temp as h48_air_temp
			, hist_pred_48h.precipitation_amount as h48_precipitation_amount
			, hist_pred_48h.wind_bearing as h48_wind_bearing
			, null as h48_wind_bearing_sin
            , null as h48_wind_bearing_cos
			, hist_pred_48h.wind_speed as h48_wind_speed
			, hist_pred_48h.cloud_area_fraction as h48_cloud_area_fraction
			, hist_pred_48h.air_pressure_at_sea_level as h48_air_pressure_at_sea_level
			, hist_pred_48h.relative_humidity as h48_relative_humidity
			, hist_pred_54h.air_temp as h54_air_temp
			, hist_pred_54h.precipitation_amount as h54_precipitation_amount
			, hist_pred_54h.wind_bearing as h54_wind_bearing
            , null as h54_wind_bearing_sin
            , null as h54_wind_bearing_cos
			, hist_pred_54h.wind_speed as h54_wind_speed
			, hist_pred_54h.cloud_area_fraction as h54_cloud_area_fraction
			, hist_pred_54h.air_pressure_at_sea_level as h54_air_pressure_at_sea_level
			, hist_pred_54h.relative_humidity as h54_relative_humidity
            , nullif(hist_obs_00.air_temp, 99) obs00_air_temp
            , nullif(hist_obs_00.relative_humidity, 100) obs00_relative_humidity
            , nullif(hist_obs_00.dew_point_temp, 99) obs00_dew_point_temp
            , nullif(hist_obs_00.wind_speed, 99) obs00_wind_speed
            , nullif(hist_obs_00.wind_bearing, 999) obs00_wind_bearing
            , nullif(hist_obs_00.min_visibility_dist, 99999) obs00_min_visibility_dist
            , hist_obs_00.precipitation_intensity obs00_precipitation_intensity
            , nullif(hist_obs_00.road_temp, 99) obs00_road_temp
			, nullif(hist_obs_06.air_temp, 99) obs06_air_temp
            , nullif(hist_obs_06.relative_humidity, 100) obs06_relative_humidity
            , nullif(hist_obs_06.dew_point_temp, 99) obs06_dew_point_temp
            , nullif(hist_obs_06.wind_speed, 99) obs06_wind_speed
            , nullif(hist_obs_06.wind_bearing, 999) obs06_wind_bearing
            , nullif(hist_obs_06.min_visibility_dist, 99999) obs06_min_visibility_dist
            , hist_obs_06.precipitation_intensity obs06_precipitation_intensity
            , nullif(hist_obs_06.road_temp, 99) obs06_road_temp
            , nullif(hist_obs_12.air_temp, 99) obs12_air_temp
            , nullif(hist_obs_12.relative_humidity, 100) obs12_relative_humidity
            , nullif(hist_obs_12.dew_point_temp, 99) obs12_dew_point_temp
            , nullif(hist_obs_12.wind_speed, 99) obs12_wind_speed
            , nullif(hist_obs_12.wind_bearing, 999) obs12_wind_bearing
            , nullif(hist_obs_12.min_visibility_dist, 99999) obs12_min_visibility_dist
            , hist_obs_12.precipitation_intensity obs12_precipitation_intensity
            , nullif(hist_obs_12.road_temp, 99) obs12_road_temp
			, nullif(hist_obs_18.air_temp, 99) obs18_air_temp
            , nullif(hist_obs_18.relative_humidity, 100) obs18_relative_humidity
            , nullif(hist_obs_18.dew_point_temp, 99) obs18_dew_point_temp
            , nullif(hist_obs_18.wind_speed, 99) obs18_wind_speed
            , nullif(hist_obs_18.wind_bearing, 999) obs18_wind_bearing
            , nullif(hist_obs_18.min_visibility_dist, 99999) obs18_min_visibility_dist
            , hist_obs_18.precipitation_intensity obs18_precipitation_intensity
            , nullif(hist_obs_18.road_temp, 99) obs18_road_temp
            , ifnull(snow_observations.Snødybde, 0) snow_depth 
			, case when closed_hist0d.Date is not null then closed_hist0d.Stengt_00_06 else 0 end as d0_stengt_00_06
            , case when closed_hist0d.Date is not null then closed_hist0d.Stengt_06_12 else 0 end as d0_stengt_06_12
			, case when closed_hist0d.Date is not null then closed_hist0d.Stengt_12_18 else 0 end as d0_stengt_12_18
            , case when closed_hist0d.Date is not null then closed_hist0d.Stengt_18_24 else 0 end as d0_stengt_18_24
			, case when closed_hist1d.Date is not null then closed_hist1d.Stengt_00_06 else 0 end as d1_stengt_00_06
            , case when closed_hist1d.Date is not null then closed_hist1d.Stengt_06_12 else 0 end as d1_stengt_06_12
			, case when closed_hist1d.Date is not null then closed_hist1d.Stengt_12_18 else 0 end as d1_stengt_12_18
            , case when closed_hist1d.Date is not null then closed_hist1d.Stengt_18_24 else 0 end as d1_stengt_18_24
			, case when closed_hist2d.Date is not null then closed_hist2d.Stengt_00_06 else 0 end as d2_stengt_00_06
            , case when closed_hist2d.Date is not null then closed_hist2d.Stengt_06_12 else 0 end as d2_stengt_06_12
			, case when closed_hist2d.Date is not null then closed_hist2d.Stengt_12_18 else 0 end as d2_stengt_12_18
            , case when closed_hist2d.Date is not null then closed_hist2d.Stengt_18_24 else 0 end as d2_stengt_18_24

		from vegvarsel.datelist dates
		inner join vegvarsel.historic_weather_predictions hist_pred_6h on dates.thedate = Date(hist_pred_6h.forecast_ref_time) and hist_pred_6h.forecast_time = 6 and hist_pred_6h.station_id = station_id
		inner join vegvarsel.historic_weather_predictions hist_pred_12h on dates.thedate = Date(hist_pred_12h.forecast_ref_time) and hist_pred_12h.forecast_time = 12 and hist_pred_12h.station_id = station_id
		inner join vegvarsel.historic_weather_predictions hist_pred_18h on dates.thedate = Date(hist_pred_18h.forecast_ref_time) and hist_pred_18h.forecast_time = 18 and hist_pred_18h.station_id = station_id
		inner join vegvarsel.historic_weather_predictions hist_pred_24h on dates.thedate = Date(hist_pred_24h.forecast_ref_time) and hist_pred_24h.forecast_time = 24 and hist_pred_24h.station_id = station_id
		inner join vegvarsel.historic_weather_predictions hist_pred_30h on dates.thedate = Date(hist_pred_30h.forecast_ref_time) and hist_pred_30h.forecast_time = 30 and hist_pred_30h.station_id = station_id
		inner join vegvarsel.historic_weather_predictions hist_pred_36h on dates.thedate = Date(hist_pred_36h.forecast_ref_time) and hist_pred_36h.forecast_time = 36 and hist_pred_36h.station_id = station_id
		inner join vegvarsel.historic_weather_predictions hist_pred_42h on dates.thedate = Date(hist_pred_42h.forecast_ref_time) and hist_pred_42h.forecast_time = 42 and hist_pred_42h.station_id = station_id
		left join vegvarsel.historic_weather_predictions hist_pred_48h on dates.thedate = Date(hist_pred_48h.forecast_ref_time) and hist_pred_48h.forecast_time = 48 and hist_pred_48h.station_id = station_id
        left join vegvarsel.historic_weather_predictions hist_pred_54h on dates.thedate = Date(hist_pred_54h.forecast_ref_time) and hist_pred_54h.forecast_time = 54 and hist_pred_54h.station_id = station_id
        left join vegvarsel.historic_weather_observations hist_obs_00 on dates.thedate = Date(hist_obs_00.observation_time) and hour(hist_obs_00.observation_time) = 0 and hist_obs_00.road_id = (select road_id from vegvarsel.road_information where station_id = station_id limit 1)
        left join vegvarsel.historic_weather_observations hist_obs_06 on dates.thedate = Date(hist_obs_06.observation_time) and hour(hist_obs_06.observation_time) = 0 and hist_obs_06.road_id = (select road_id from vegvarsel.road_information where station_id = station_id limit 1)
        left join vegvarsel.historic_weather_observations hist_obs_12 on dates.thedate = Date(hist_obs_12.observation_time) and hour(hist_obs_12.observation_time) = 0 and hist_obs_12.road_id = (select road_id from vegvarsel.road_information where station_id = station_id limit 1)
        left join vegvarsel.historic_weather_observations hist_obs_18 on dates.thedate = Date(hist_obs_18.observation_time) and hour(hist_obs_18.observation_time) = 0 and hist_obs_18.road_id = (select road_id from vegvarsel.road_information where station_id = station_id limit 1)
        left join vegvarsel.snow_depth_observations snow_observations on dates.thedate = DATE_ADD(DATE_ADD(MAKEDATE(snow_observations.år, 1), INTERVAL (snow_observations.måned)-1 MONTH), INTERVAL (snow_observations.Dag)-1 DAY) and snow_observations.Station_id = station_id
		left join vegvarsel.closed_road_history closed_hist0d on Date(dates.thedate) = Date(closed_hist0d.Date) and closed_hist0d.station_id = station_id
		left join vegvarsel.closed_road_history closed_hist1d on Date_Add(Date(dates.thedate), INTERVAL 1 DAY) = Date(closed_hist1d.Date) and closed_hist1d.station_id = station_id
		left join vegvarsel.closed_road_history closed_hist2d on Date_Add(Date(dates.thedate), INTERVAL 2 DAY) = Date(closed_hist2d.Date) and closed_hist2d.station_id = station_id
		;

Drop temporary table vegvarsel.datelist;
END