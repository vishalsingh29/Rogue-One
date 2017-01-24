
FABRIC_DOCTOR_QUERY = """
select
  distinct  up.account_id from fabric.practices_published p
  inner join fabric.practice_doctors_published pd on pd.practice_id=p.id
  inner join fabric.doctors_published d on d.id = pd.doctor_id
  inner join fabric.doctor_verification_statuses_published dv on dv.doctor_id = d.id
  inner join fabric.master_localities ml on ml.id= p.locality_id
  inner join fabric.master_cities mc on mc.id = ml.city_id
  inner join fabric.master_states ms on ms.id = mc.state_id
  inner join fabric.master_countries mcc on mcc.id = ms.country_id
  inner join fabric.user_profile up on up.id = d.user_id

  left join fabric.practice_types_published pt on pt.practice_id=p.id
  left join fabric.master_practice_types mpt on mpt.id = pt.types_id
  where p.deleted_at is null and pd.deleted_at is null and dv.deleted_at is null and pd.profile_published =1
  and ml.deleted_at is null   and pt.deleted_at is null   and d.deleted_at is null and mpt.deleted_at is null
  and (mpt.name = 'Hospital'  or mpt.name = 'Clinic'  or pt.types_id is null)
  and dv.verification_status = 'VERIFIED' and p.demo = 0  and mcc.name = 'India'
  and p.has_active_ray_subscription = 1
  and p.deleted_at is null
  and pd.status in ('ABS','abs')
"""
