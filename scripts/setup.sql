alter table modules add convener_usernames text;
alter table modules drop row_id;

create table convenes
(
    staff_username text not null
        constraint convenes_staff_username_fk
            references staff,
    module_code    text not null
        constraint convenes_modules_code_fk
            references modules,
    PRIMARY KEY (staff_username, module_code)
);
