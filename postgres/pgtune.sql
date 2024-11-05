-- DB Version: 17
-- OS Type: linux
-- DB Type: dw
-- Total Memory (RAM): 2 GB
-- CPUs num: 2
-- Data Storage: ssd
-- https://pgtune.leopard.in.ua/?dbVersion=17&osType=linux&dbType=dw&cpuNum=2&totalMemory=2&totalMemoryUnit=GB&connectionNum=&hdType=ssd

ALTER SYSTEM SET
 max_connections = '40';
ALTER SYSTEM SET
 shared_buffers = '512MB';
ALTER SYSTEM SET
 effective_cache_size = '1536MB';
ALTER SYSTEM SET
 maintenance_work_mem = '256MB';
ALTER SYSTEM SET
 checkpoint_completion_target = '0.9';
ALTER SYSTEM SET
 wal_buffers = '16MB';
ALTER SYSTEM SET
 default_statistics_target = '500';
ALTER SYSTEM SET
 random_page_cost = '1.1';
ALTER SYSTEM SET
 effective_io_concurrency = '200';
ALTER SYSTEM SET
 work_mem = '3276kB';
ALTER SYSTEM SET
 huge_pages = 'off';
ALTER SYSTEM SET
 min_wal_size = '4GB';
ALTER SYSTEM SET
 max_wal_size = '16GB';