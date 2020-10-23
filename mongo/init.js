db.auth('admin', 'admin')

var upa = db.getSiblingDB('upa')

upa.createUser({
  user: 'scraper',
  pwd: 'scraper',
  roles: [
    {
      role: 'readWrite',
      db: 'upa',
    },
    {
      role: 'dbAdmin',
      db: 'upa',
    },
  ],
});

upa.createUser({
  user: 'computer',
  pwd: 'computer',
  roles: [
    {
      role: 'read',
      db: 'upa',
    },
  ],
});

upa.delete_me.insertOne({right: 'now'})