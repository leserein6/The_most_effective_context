# 微服务全景图

来源为用户提供的工程能力分类。可直接用于定位任务或选择调查种子。映射实际系统时，标出由服务代码、框架或基础设施承担的部分，附对应版本的依据。

| 能力域 | 子项（保留原顺序） |
|---|---|
| 1. 服务运行与生命周期 | 进程启动、Boot / Init、依赖初始化、Server 启动、后台任务、优雅退出 |
| 2. 接口与服务通信 | RPC、HTTP、IDL / Proto、序列化 / 反序列化、Frame / Codec、Client Stub、Server Handler |
| 3. 注册发现与流量路由 | 服务注册、服务发现、健康检查、实例元数据、路由、负载均衡、流量染色 / 泳道 / 灰度 |
| 4. 服务治理 | Timeout、Retry、限流、熔断、降级、隔离、容灾 / Failover / Escape |
| 5. 配置与控制 | 本地配置、配置中心、配置加载、动态配置、开关、热更新、配置容灾 / 本地缓存 |
| 6. 数据与外部依赖 | DB、Cache、MQ、下游 RPC、公共库、SDK、Agent / Sidecar |
| 7. 可观测性 | Logging、Metrics、Tracing、Event、Dashboard、Alert |
| 8. 部署与运行环境 | Process、Container、Pod、Node、Kubernetes、网络与存储、扩缩容 / 多机房部署 |
| 9. 发布、测试与安全 | Build、CI / CD、发布、灰度、回滚、测试体系、压测、鉴权 / 权限 / TLS |
