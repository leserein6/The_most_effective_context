---
name: trpc-go-review
description: Go 服务的 tRPC-Go 或其他明确 RPC 框架代码审查，尤其是 Handler 注册、Filter 链、Proxy/连接复用、context/deadline、错误码、重试、路由和 Protobuf 兼容性。按需追加在通用 Go Review 之后。
allowed-tools: Read, Grep, Glob
---

# RPC / tRPC-Go 专项 Review

**来源：** 用户历史 `trpc-go-review.md` 经核查、去重与边界修正后的可复用专项。通用 Go 语义只在 [go-review](../go-review/SKILL.md) 检查；不要重复给同一风险两份 Finding。

## 第一步：核实框架和最小请求路径

- 看当前仓库真实依赖、协议文件、生成代码、启动与注册入口；**tRPC-Go 的实际行为依赖版本和配置**，不能从类名或经验推断。
- 对一个受影响接口追踪 `入站/解码 → Server Filter → Handler → 业务 → 下游 Proxy/Client Filter → 回包/错误`；框架无法访问的层标未验证。
- 关注请求发起者、地址/路由选择、超时/取消、序列化及错误的实际观察位置。不要用通用示意图冒充源码真实执行顺序。

## 根据触发面检查

1. **注册和启动**：服务是否正确注册、Handler 与协议是否匹配、初始化失败会不会留下可服务的半初始化状态。
2. **Proxy/Client 生命周期**：是否有不必要的重复构造或连接，框架是否已经管理池化；先确认 API 契约，不能仅凭每次调用 `NewProxy` 就认定泄漏。
3. **Context 和时限**：上游 deadline、下游时限、取消与 Metadata/Trace 如何传播；超时预算与实际工作耗时是否冲突，**不强制所有服务必须形成固定的大小关系**。
4. **重试与不确定结果**：框架/业务各自重试了什么错误；重复放大、调用是否幂等；timeout 并不表示下游肯定未执行。
5. **错误链和返回契约**：transport / framework / business code 分开；包装转换后调用方还能否判断？`err != nil`、响应字段及出域消息如何配合。
6. **Codec/Protobuf**：字段兼容、proto2/proto3、optional/presence、缺省值、未知字段、旧客户端行为。可得时比对实际协议版本。
7. **Filter / 中间件**：顺序与返回链、panic/鉴权/监控、错误和 Context 是否被修改；确认注册顺序与框架实现。
8. **注册发现/路由/负载均衡**：服务名、配置优先级、直连或 Relay 等实际路径；区分 discovery、route、selector、transport。
9. **可观测性与退出**：Trace、结构化错误、敏感日志、in-flight 排空、连接/资源清理与超时退出。

## 输出

只报告本次变更/调用链相关的可证伪问题：`RPC 阶段 | 真实路径 | 失败条件 | 影响 | 证据 | 建议的验证`。框架外部依赖无法查看时列「需要该版本源码/配置」，禁止写成已确认。审查后将结论交还主 Reviewer，不写 Project、测试代码或 Git 变更。
