alter table modules drop row_id;

create table convenes
(
    staff_username text not null
        constraint convenes_staff_username_fk
            references staff,
    module_code    text not null
        constraint convenes_modules_code_fk
            references modules,
    primary key (staff_username, module_code)
);

create table unknown_conveners
(
    name        text not null primary key,
    module_code text not null
        constraint unknown_conveners_modules_code_fk
            references modules
)
