# Task [P2]: Hardening & Admin Features

## Goal

Enhance system security, monitoring, and provide admin tools for content management.

> [!NOTE]
> **Agent Skills Utilized**: [Security Audit](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/security/aws-security-audit/SKILL.md), [Performance Engineer](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/performance-engineer/SKILL.md), [Systematic Debugging](file:///e:/my-pj/learn-python/E-commerce-platforms/Front-end/ecommerce-next/.agent/skills/plugins/antigravity-awesome-skills-claude/skills/systematic-debugging/SKILL.md)

## Sub-tasks

### [P2-01] Cloudinary Integration (Media)

- **Feature**: Automatic upload of product images to Cloudinary.
- **Config**: Setup `django-cloudinary-storage`.

### [P2-02] Sentry & Monitoring

- **Feature**: Track production errors and performance.
- **Config**: Initialize `sentry-sdk` in `settings.py`.

### [P2-03] Admin Dashboard APIs (Analytics)

- **Feature**: Summary of sales, top products, user growth.
- **Permission**: `IsAdminUser` only.

### [P2-04] Security Hardening

- **Feature**: Rate limiting (DRF Throttling), CORS policy refinement, secure headers.

## Reference

- [04-permission-matrix.md](./04-permission-matrix.md)
- [03-technical-stack-skills-and-versions.vi.md](../03-technical-stack-skills-and-versions.vi.md)
